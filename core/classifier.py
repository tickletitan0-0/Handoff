# core/classifier.py
TIP_IDS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky tips

NUMBER_NAMES = {
    0: "ZERO",
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
}


def _dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def fingers_up(landmarks, handedness="Right"):
    """Returns a list of 5 booleans: [thumb, index, middle, ring, pinky]"""
    if not landmarks or len(landmarks) < 21:
        return [False] * 5

    fingers = []

    # Thumb: normalized distance check (tip-to-index-MCP vs hand size)
    # rather than a bare x-sign comparison, since a curled thumb can
    # still show a tiny x-delta and read as falsely "extended".
    wrist = landmarks[0]
    middle_mcp = landmarks[9]
    hand_size = _dist(wrist, middle_mcp) or 1e-6  # avoid div-by-zero

    thumb_tip = landmarks[TIP_IDS[0]]
    index_mcp = landmarks[5]
    thumb_extended = _dist(thumb_tip, index_mcp) > 0.6 * hand_size
    fingers.append(thumb_extended)

    # Other four fingers: compare y-coordinates (tip above pip = extended)
    for tip_id in TIP_IDS[1:]:
        tip_y = landmarks[tip_id][1]
        pip_y = landmarks[tip_id - 2][1]
        fingers.append(tip_y < pip_y)

    return fingers


def classify_gesture(landmarks, handedness="Right"):
    """Returns a numeric gesture name based on how many fingers are
    extended: ZERO, ONE, TWO, THREE, FOUR, or FIVE.
    """
    if not landmarks:
        return "ZERO"

    fingers = fingers_up(landmarks, handedness)
    count = sum(fingers)
    return NUMBER_NAMES[count]