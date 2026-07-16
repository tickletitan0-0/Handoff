import cv2

class CameraStream:
    def __init__(self, source=0, width=640, height=480):
        self.cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, 30);
    def read(self):
        ok, frame = self.cap.read()
        if not ok:
            return None
        #mirroring screen so that hand appears on intended side
        frame = cv2.flip(frame, 1)
        return frame
    
    def release(self):
        self.cap.release()