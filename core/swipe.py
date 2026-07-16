# core/swipe.py
import time


class SwipeDetector:
    """Tracks wrist x-position over a short time window to detect a
    left-to-right swipe. Static-pose gestures (classifier.py) can't
    express motion gestures like SWIPE_RIGHT, so this runs alongside
    the classifier and feeds its own result into the same debouncer.
    """

    def __init__(self, window_seconds=0.6, min_dx_ratio=1.2, cooldown=2.0,
                 max_missed_frames=5, debug=False):
        self.window_seconds = window_seconds
        self.min_dx_ratio = min_dx_ratio
        self.cooldown = cooldown
        # Fast swipes cause motion blur, and Mediapipe frequently loses
        # tracking for a frame or two mid-motion (much more than it does
        # for a held static pose). Clearing history on every single miss
        # fragmented the swipe into pieces too short to ever cross the
        # threshold. Now we only give up after several consecutive
        # missed frames.
        self.max_missed_frames = max_missed_frames
        self.debug = debug
        self._history = []  # list of (timestamp, wrist_x, hand_size)
        self._last_fired_at = 0.0
        self._missed_frames = 0

    def update(self, landmarks):
        now = time.time()

        if not landmarks or len(landmarks) < 21:
            self._missed_frames += 1
            if self._missed_frames > self.max_missed_frames:
                self._history.clear()
            return None
        self._missed_frames = 0

        if (now - self._last_fired_at) < self.cooldown:
            # Still cooling down from the last swipe; keep tracking
            # position so we don't get a stale/huge dx once cooldown
            # ends, but don't fire again yet.
            self._history.append((now, landmarks[0][0], 1.0))
            self._history = [h for h in self._history if now - h[0] <= self.window_seconds]
            return None

        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        hand_size = (
            (wrist[0] - middle_mcp[0]) ** 2 + (wrist[1] - middle_mcp[1]) ** 2
        ) ** 0.5 or 1e-6

        self._history.append((now, wrist[0], hand_size))
        self._history = [h for h in self._history if now - h[0] <= self.window_seconds]

        if len(self._history) < 2:
            return None

        # Use the leftmost x seen within the window rather than just the
        # oldest entry, so a small backward jitter at the start of the
        # swipe doesn't undercount the real displacement.
        start_x = min(h[1] for h in self._history)
        dx = wrist[0] - start_x
        threshold = self.min_dx_ratio * hand_size

        if self.debug:
            print(f"[swipe] dx={dx:.1f} threshold={threshold:.1f} "
                  f"hand_size={hand_size:.1f} samples={len(self._history)}")

        if dx > threshold:
            self._history.clear()
            self._last_fired_at = now
            return "SWIPE_RIGHT"

        return None