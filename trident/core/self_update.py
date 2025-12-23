from __future__ import annotations

import subprocess
import sys
from typing import Dict, Any

from trident.identity import get_version, get_timestamp
from trident.logging import log, log_section
from trident.core.channel import validate_channel, resolve_docker_tag


def run_self_update(apply: bool = False, channel: str = "stable") -> Dict[str, Any]:
    """
    Self-update logic with channel support.

    Channels:
      - stable
      - edge
      - dev
    """
    log_section("Self-Update Check")

    # Validate and resolve channel
    channel = validate_channel(channel)
    tag = resolve_docker_tag(channel)
    image = f"notchofhwend/updater:{tag}"

    result: Dict[str, Any] = {
        "timestamp": get_timestamp(),
        "channel": channel,
        "docker_image": image,
        "applied": False,
    }

    if apply:
        try:
            log("Pulling updater image", context={"image": image})
            subprocess.check_call(["docker", "pull", image])

            log("Running updater container", context={"image": image})
            subprocess.check_call(["docker", "run", "--rm", image])

            result["applied"] = True
            log("Self-update applied", context=result)

        except Exception as exc:
            msg = str(exc)
            log("Self-update failed", level="ERROR", context={"error": msg})
            result["error"] = msg

    return result
