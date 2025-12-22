"""
logging.py — Deterministic Logging for The Veil
-----------------------------------------------

Provides a minimal, timestamped logging utility that writes to logs/veil.log.
This module avoids external dependencies and ensures consistent formatting.
"""

from pathlib import Path
from identity import get_timestamp, get_project_root


# ------------------------------------------------------------
# 🔱 Log File Setup
# ------------------------------------------------------------

def _log_path() -> Path:
    root = get_project_root()
    logs_dir = root / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir / "veil.log"


# ------------------------------------------------------------
# 🔱 Logging API
# ------------------------------------------------------------

def log(message: str) -> None:
    """
    Writes a timestamped log entry to logs/veil.log.
    """
    entry = f"{get_timestamp()} — {message}\n"
    path = _log_path()

    with path.open("a", encoding="utf-8") as f:
        f.write(entry)


def log_section(title: str) -> None:
    """
    Writes a section header to the log for readability.
    """
    log(f"--- {title} ---")


# ------------------------------------------------------------
# 🔱 CLI Preview
# ------------------------------------------------------------

if __name__ == "__main__":
    log_section("Logging Test")
    log("This is a test log entry.")
    print("Log entry written to logs/veil.log")
