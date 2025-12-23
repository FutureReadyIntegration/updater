from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from trident.core.channel import validate_channel

CONFIG_DIR = Path.home() / ".trident"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "channel": "stable"
}


def load_config() -> Dict[str, Any]:
    """
    Load the user's config file, or return defaults if missing.
    """
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()

    try:
        data = json.loads(CONFIG_FILE.read_text())
        # Validate channel
        data["channel"] = validate_channel(data.get("channel", "stable"))
        return data
    except Exception:
        # If config is corrupted, fall back to defaults
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    """
    Save the config file, creating directories if needed.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def get_default_channel() -> str:
    """
    Return the configured default channel.
    """
    return load_config().get("channel", "stable")


def set_default_channel(channel: str) -> Dict[str, Any]:
    """
    Update the default channel in the config file.
    """
    channel = validate_channel(channel)
    config = load_config()
    config["channel"] = channel
    save_config(config)
    return config
