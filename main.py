import time
from core.capture import CameraStream
from core.detector import HandDetector
from core.classifier import classify_gesture
from core.debounce import GestureDebouncer
from core.actions import execute_binding
from core.config_loader import load_config

def run(show_debug_window=False):
    cfg = load_config()
    cam = CameraStream(source=cfg["camera_index"])
    detector = HandDetector()
    debouncer = GestureDebouncer(
        hold_frames = cfg["hold_frames_required"],
        cooldown = cfg["cooldown_seconds"]
    )

    running = True

    while running:
        frame = cam.read()
        if frame is None:
            time.sleep(0.05)
            continue

        landmarks, frame = detector.find_hands(frame, draw=show_debug_window)
        gesture = classify_gesture(landmarks) if landmarks else "NONE"

        confirmed = debouncer.update(gesture)
        if confirmed and confirmed in cfg["bindings"]:
            execute_binding(cfg["bindings"][confirmed])

        if show_debug_window:
            import cv2
            cv2.imshow("Gesture Debug", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                running = False

    cam.release()

if __name__ == "__main__":
    run(show_debug_window=False)