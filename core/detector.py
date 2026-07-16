import mediapipe as mp
import cv2

class HandDetector:
    def __init__(self, max_hands=1, detection_conf=0.7, tracking_conf=0.6):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode = False,
            max_num_hands = max_hands,
            min_detection_confidence = detection_conf,
            min_tracking_confidence = tracking_conf
        )
        self.mp_hands = mp.solutions.drawing_utils

    def find_hands(self, frame_bgr, draw=False):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        landmark_list = []
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h,w, _ = frame_bgr.shape
            for lm in hand.landmark:
                landmark_list.append((lm.x * w, lm.y * h, lm.z))
            if draw:
                self.mp_draw.draw_landmarks(frame_bgr, hand, self.mp_hands.HAND_CONNECTIONS)

        return landmark_list, frame_bgr
