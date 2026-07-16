TIP_IDS = [4,8,12,16,20]

def fingers_up(landmarks, handedness="Right"):
    if not landmarks:
        return [False]*5
    
    fingers = []

    if handedness == "Right":
        fingers.append(landmarks[TIP_IDS[0][0] > landmarks[TIP_IDS[0]-1][0]])
    else:
        fingers.append(landmarks[TIP_IDS[0][0] < landmarks[TIP_IDS[0]-1][0]])
    
    for tip_id in TIP_IDS[1:]:
        fingers.append(landmarks[tip_id][1] < landmarks[tip_id-2][1])
    
    return fingers

def classify_gesture(landmarks, handedness = "Right"):
    fingers = fingers_up(landmarks, handedness)
    thumb, index, middle, ring, pinky = fingers

    if all(fingers):
        return "OPEN_PALM"
    
    if not any(fingers):
        return "FIST"
    
    if index and middle and not ring and not pinky and not thumb:
        return "PEACE"
    
    if index and not middle and not ring and not pinky:
        return "POINT"
    
    if thumb and not index and not middle and not ring and not pinky:
        return "THUMBS_UP"
    
    if pinky and thumb and not index and not middle and not ring:
        return "CALL_ME"
    
    return "UNKNOWN"

class SwipeDetector:
    def __init__(self, history_len=8, threshold_px=120):
        self.history = []
        self.history_len = history_len
        self.threshold_px = threshold_px

    def update(self, wrist_x):
        self.history.append(wrist_x)
        if len(self.history) > self.history_len:
            self.history.pop(0)

        if len(self.history) == self.history_len:
            delta = self.history[-1] - self.history[0]
            if delta > self.threshold_px:
                return "SWIPE_RIGHT"
            if delta <  self.threshold_px:
                return "SWIPE_LEFT"
            
        return None
