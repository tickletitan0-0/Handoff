# core/detector.py
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

class HandDetector:
    def __init__(self, model_path="hand_landmarker.task", max_hands=1,
                 detection_conf=0.7, tracking_conf=0.6):
        base_options = mp_python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self._timestamp_ms = 0

    def find_hands(self, frame_bgr, draw=False):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        self._timestamp_ms += 33  # ~30fps step; must be strictly increasing
        result = self.landmarker.detect_for_video(mp_image, self._timestamp_ms)

        landmark_list = []
        handedness = "Right"
        if result.hand_landmarks:
            h, w, _ = frame_bgr.shape
            hand = result.hand_landmarks[0]  # first detected hand
            for lm in hand:
                landmark_list.append((lm.x * w, lm.y * h, lm.z))

            if result.handedness:
                handedness = result.handedness[0][0].category_name

            if draw:
                for x, y, _ in landmark_list:
                    cv2.circle(frame_bgr, (int(x), int(y)), 4, (0, 255, 0), -1)

        return landmark_list, frame_bgr, handedness

    def close(self):
        self.landmarker.close()