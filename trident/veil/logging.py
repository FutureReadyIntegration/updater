from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .identity import get_project_root


def _get_log_directory() -> Path:
    """
    Return the canonical log directory for The Veil.

    We keep logs at:
        <project_root>/logs/

    This ensures logs are outside the package directory and easy to rotate or inspect.
    """
    root = get_project_root()
    log_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def _get_log_file() -> Path:
    """
    Return the primary log file path.

    Currently:
        <project_root>/logs/veil.log
    """
    return _get_log_directory() / "veil.log"


def _serialize_log_record(record: Dict[str, Any]) -> str:
    """
    Serialize a log record as a single-line JSON string.

    This is intentionally minimal and deterministic.
    """
    return json.dumps(record, sort_keys=True)


def log(
    message: str,
    level: str = "INFO",
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Append a JSON log entry to the primary log file.

    Args:
        message: Human-readable message.
        level: Log level (INFO, WARN, ERROR, DEBUG).
        context: Optional dict with extra fields.
    """
    context = context or {}
    record: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level.upper(),
        "message": message,
    }
    record.update(context)

    log_file = _get_log_file()
    line = _serialize_log_record(record) + "\n"

    # Append mode; if file doesn't exist it will be created.
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as f:
        f.write(line)


def log_section(title: str) -> None:
    """
    Write a structural separator into the log for readability.

    Args:
        title: Section title.
    """
    log(f"--- {title} ---", level="INFO")
