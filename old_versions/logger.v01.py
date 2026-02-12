import os
from datetime import datetime

LOG_ROOT = "logs"


def get_day_dir():
    """Return path like logs/YYYY-MM-DD (no creation yet)."""
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_ROOT, today)


def ensure_day_dir():
    """1. If logs/[day] does not exist: create the missing folder."""
    day_dir = get_day_dir()
    os.makedirs(day_dir, exist_ok=True)
    return day_dir


def get_session_filename():
    """Return full path for a unique session file inside today's folder."""
    day_dir = ensure_day_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = f"session-{timestamp}.md"
    return os.path.join(day_dir, filename)


def start_session():
    """Create a new session .md file and write a header; return its path."""
    path = get_session_filename()

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Chat session\n\n")
        f.write(f"- Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"- Started at: {datetime.now().strftime('%H:%M:%S')}\n\n")
        f.write("---\n\n")

    return path


def log_message(path, role, content):
    """
    1. Ensure logs/[day] folder exists.
    2. Then append the message.
    """
    # 1. If folder/[day] does not exist: create the missing folder.
    day_dir = ensure_day_dir()

    # (extra safety) make sure the session file's parent matches and exists
    os.makedirs(os.path.dirname(path) or day_dir, exist_ok=True)

    # 2. Run log_message(): append to file
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"**{role}:** {content}\n\n")
