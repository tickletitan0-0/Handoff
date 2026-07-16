import json
import os


def load_config(path="config.json"):
    # A bare relative path only resolves correctly if the script's
    # current working directory happens to be its own folder. That's
    # true when you run `python main.py` from inside the project dir,
    # but breaks if this is ever launched another way (shortcut,
    # startup folder, scheduled task, double-click from elsewhere).
    # Falling back to a path next to this file makes it resolve
    # consistently regardless of cwd, while still honoring an
    # explicit path if one is passed in.
    if not os.path.isabs(path) and not os.path.exists(path):
        candidate = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        if os.path.exists(candidate):
            path = candidate

    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    # Fixed typo: was "cooldown seconds" (space), which silently created
    # an unused key instead of ever providing a real fallback.
    cfg.setdefault("cooldown_seconds", 2.0)
    cfg.setdefault("hold_frames_required", 6)

    return cfg