import time

class GestureDebouncer:
    def __init__(self, hold_frames = 0, cooldown = 2.0):
        self.hold_frames = hold_frames
        self.cooldown = cooldown
        self._current_gesture = None
        self._current_count = 0
        self._last_fired_at = 0.0

    def update(self, gesture:str):
        if gesture == self._current_gesture:
            self._current_count+=1
        else:
            self._current_gesture = gesture
            self._current_count = 1
        
        now = time.time()
        cooldown_ok = (now - self._last_fired_at)>=self.cooldown
        # Was `== self.hold_frames`, which requires the count to land on
        # that exact frame. Any jitter (a single dropped/misclassified
        # frame) resets the counter and the count can sail past
        # hold_frames without ever equaling it again, so the gesture
        # never fires. `>=` fires as soon as the hold requirement is
        # met and keeps firing correctly with the cooldown guard below.
        stable_enough = self._current_count >= self.hold_frames

        if gesture not in (None, "NONE", "UNKNOWN") and stable_enough and cooldown_ok:
            self._last_fired_at = now
            return gesture
        
        return None