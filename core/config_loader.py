import json

def load_config(path = "config.json"):
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("cooldown seconds", 2.0)
    cfg.setdefault("hold_frames_required", 6.0)

    return cfg