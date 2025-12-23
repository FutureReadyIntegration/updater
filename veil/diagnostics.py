from __future__ import annotations

import platform
import sys
from pathlib import Path
from typing import Any, Dict, List

from .identity import get_project_root, get_timestamp, get_version
from .logging import log, log_section


def _check_python_version() -> Dict[str, Any]:
    version_info = sys.version_info
    ok = version_info.major == 3 and version_info.minor >= 8
    return {
        "name": "python_version",
        "ok": ok,
        "current": f"{version_info.major}.{version_info.minor}.{version_info.micro}",
        "required": ">= 3.8",
    }


def _check_venv() -> Dict[str, Any]:
    in_venv = (
        hasattr(sys, "base_prefix")
        and sys.prefix != sys.base_prefix
    ) or bool(getattr(sys, "real_prefix", None))

    return {
        "name": "virtual_environment",
        "ok": in_venv,
        "current": sys.prefix,
        "required": "Active virtualenv recommended",
    }


def _check_paths() -> Dict[str, Any]:
    root = get_project_root()
    pyproject = root / "pyproject.toml"
    logs_dir = root / "logs"

    return {
        "name": "project_paths",
        "ok": pyproject.exists(),
        "project_root": str(root),
        "pyproject_exists": pyproject.exists(),
        "logs_dir": str(logs_dir),
    }


def _check_platform() -> Dict[str, Any]:
    return {
        "name": "platform",
        "ok": True,
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
    }


def _format_result(result: Dict[str, Any]) -> str:
    status = "OK" if result.get("ok") else "WARN"
    parts = [f"[{status}] {result.get('name', 'unknown')}"]

    for key, value in result.items():
        if key in ("name", "ok"):
            continue
        parts.append(f"    {key}: {value}")

    return "\n".join(parts)


def run_diagnostics() -> Dict[str, Any]:
    """
    Run a suite of diagnostics checks and return a structured result.

    This function is used by the CLI and may also be imported programmatically.
    """
    log_section("Diagnostics Run")

    checks: List[Dict[str, Any]] = [
        _check_python_version(),
        _check_venv(),
        _check_paths(),
        _check_platform(),
    ]

    for c in checks:
        log(
            "Diagnostic check",
            context={"name": c.get("name"), "ok": c.get("ok")},
        )

    overall_ok = all(c.get("ok", False) for c in checks)

    result: Dict[str, Any] = {
        "timestamp": get_timestamp(),
        "version": get_version(),
        "overall_ok": overall_ok,
        "checks": checks,
    }

    return result


def render_diagnostics_report(result: Dict[str, Any]) -> str:
    """
    Render a human-readable diagnostics report from the structured result.

    Args:
        result: Dict returned by run_diagnostics().

    Returns:
        str: Multi-line report.
    """
    lines: List[str] = []
    lines.append(f"Diagnostics Report — {result.get('timestamp')}")
    lines.append(f"Version: {result.get('version')}")
    lines.append(f"Overall OK: {result.get('overall_ok')}")
    lines.append("")

    for check in result.get("checks", []):
        lines.append(_format_result(check))
        lines.append("")

    return "\n".join(lines).strip()
