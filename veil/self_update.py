from __future__ import annotations

import subprocess
import sys
from typing import Dict

from .identity import get_version, get_timestamp
from .logging import log, log_section


def _get_latest_version() -> str:
    """
    Query PyPI for the latest version of trident-cli.
    """
    try:
        import requests
        response = requests.get("https://pypi.org/pypi/trident-cli/json", timeout=5)
        data = response.json()
        return data["info"]["version"]
    except Exception:
        return "unknown"


def run_self_update(apply: bool = False) -> Dict[str, str]:
    log_section("Self-Update Check")

    current = get_version()
    latest = _get_latest_version()

    result = {
        "timestamp": get_timestamp(),
        "current_version": current,
        "latest_version": latest,
        "update_available": latest != "unknown" and latest != current,
        "applied": False,
    }

    if apply and result["update_available"]:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "trident-cli"])
            result["applied"] = True
            log("Self-update applied", context=result)
        except Exception as exc:
            log("Self-update failed", level="ERROR", context={"error": str(exc)})
            result["error"] = str(exc)

    return result
