import subprocess
import sys
import os

def execute_binding(binding: dict):
    action_type = binding.get("type")
    target = binding.get("target")

    try:
        if action_type == "folder":
            _open_path(target)
        elif action_type == "app":
            _open_path(target)
        elif action_type == "command":
            subprocess.Popen(target, shell=True)
        else:
            print(f"Unknown action type: {action_type}")
    except Exception as e:
        print(f"Failed to execute binding {binding}:{e}")

def _open_path(path: str):
    if sys.platform.startswith("win"):
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])