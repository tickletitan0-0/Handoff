import cv2

cap = cv2.VideoCapture(0)
print("Camera opened:",cap.isOpened())
ret, frame = cap.read()
print("Frame shape:",frame.shape if ret else "FAILED")
cap.release()