import subprocess
import sys
import os
import webbrowser
import logging

# Errors here were only ever print()ed, which is invisible for a
# background/no-console app -- that's why failures looked like random
# silent no-ops. Logging to a file next to this script means failures
# are always recoverable after the fact.
_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "actions.log")
logging.basicConfig(
    filename=_LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def execute_binding(binding: dict):
    action_type = binding.get("type")
    target = binding.get("target")
    logging.info(f"Executing binding: type={action_type} target={target}")

    try:
        if action_type == "folder":
            _open_path(target)
        elif action_type == "app":
            _open_path(target)
        elif action_type == "command":
            _run_command(target)
        else:
            logging.warning(f"Unknown action type: {action_type}")
    except Exception as e:
        logging.error(f"Failed to execute binding {binding}: {e}", exc_info=True)


def _open_path(path: str):
    if not os.path.exists(path):
        # os.startfile raises for missing paths too, but this gives an
        # explicit, unambiguous log line instead of a bare OSError.
        logging.error(f"Path does not exist, cannot open: {path}")
        return

    if sys.platform.startswith("win"):
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def _run_command(target: str):
    # "start chrome <url>" silently fails whenever chrome.exe isn't on
    # PATH (common on Windows -- Chrome's installer doesn't add it by
    # default). Popen with shell=True doesn't raise in that case either,
    # since the shell itself launched fine; the failure happens *inside*
    # the spawned cmd.exe where Python can't see it.
    #
    # If the command is just "start <browser> <url>", open the URL
    # directly with webbrowser instead -- it uses the OS default
    # handler and doesn't depend on any executable being on PATH.
    parts = target.split()
    if len(parts) >= 3 and parts[0].lower() == "start":
        maybe_url = parts[-1]
        if maybe_url.startswith("http://") or maybe_url.startswith("https://"):
            logging.info(f"Opening URL via webbrowser: {maybe_url}")
            webbrowser.open(maybe_url)
            return

    subprocess.Popen(target, shell=True)