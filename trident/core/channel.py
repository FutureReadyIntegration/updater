from __future__ import annotations

from typing import Literal, Dict

Channel = Literal["stable", "edge", "dev"]

VALID_CHANNELS: Dict[str, str] = {
    "stable": "stable",
    "edge": "edge",
    "dev": "dev",
}


def validate_channel(channel: str) -> Channel:
    """
    Validate that the provided channel is one of the supported release channels.
    """
    channel = channel.lower().strip()
    if channel not in VALID_CHANNELS:
        raise ValueError(
            f"Invalid channel '{channel}'. Must be one of: {', '.join(VALID_CHANNELS)}"
        )
    return channel  # type: ignore[return-value]


def resolve_docker_tag(channel: Channel) -> str:
    """
    Convert a channel into the correct Docker tag.
    """
    return VALID_CHANNELS[channel]
