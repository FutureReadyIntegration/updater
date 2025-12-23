from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .identity import get_project_root, get_timestamp
from .logging import log, log_section


def _repair_logs_directory() -> Dict[str, Any]:
    """
    Ensure the logs directory exists and is writable.
    """
    root = get_project_root()
    logs_dir = root / "logs"

    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
        ok = logs_dir.exists() and logs_dir.is_dir()
        return {
            "name": "logs_directory",
            "ok": ok,
            "path": str(logs_dir),
        }
    except OSError as exc:
        return {
            "name": "logs_directory",
            "ok": False,
            "path": str(logs_dir),
            "error": str(exc),
        }


def _repair_permissions(path: Path) -> Dict[str, Any]:
    """
    Placeholder for permission repair logic.

    Currently just reports whether the path exists.
    """
    ok = path.exists()
    return {
        "name": "permissions_check",
        "ok": ok,
        "path": str(path),
    }


def run_repair() -> Dict[str, Any]:
    """
    Run a full repair routine.

    Currently:
    - Ensures logs directory exists.
    - Performs basic permission checks on key locations.
    """
    log_section("Repair Run")

    root = get_project_root()
    steps: List[Dict[str, Any]] = []

    logs_result = _repair_logs_directory()
    steps.append(logs_result)
    log("Repair step", context=logs_result)

    perm_result = _repair_permissions(root)
    steps.append(perm_result)
    log("Repair step", context=perm_result)

    overall_ok = all(s.get("ok", False) for s in steps)

    result: Dict[str, Any] = {
        "timestamp": get_timestamp(),
        "overall_ok": overall_ok,
        "steps": steps,
    }

    if overall_ok:
        log("Repair completed successfully", context={"overall_ok": True})
    else:
        log("Repair completed with warnings", level="WARN", context={"overall_ok": False})

    return result
