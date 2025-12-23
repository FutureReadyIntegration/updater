import textwrap
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Resolve the project root as the directory that contains the `veil` package.

    This assumes the standard layout:

        project_root/
            pyproject.toml
            veil/
                __init__.py
                ...

    Returns:
        Path: Absolute path to the project root directory.
    """
    return Path(__file__).resolve().parent.parent


def get_timestamp() -> str:
    """
    Return an ISO-8601 UTC timestamp string.
    """
    return datetime.utcnow().isoformat() + "Z"


def get_pyproject_path() -> Path:
    """
    Get the path to the pyproject.toml file in the project root.

    Returns:
        Path: pyproject.toml location (may not exist).
    """
    return get_project_root() / "pyproject.toml"


def get_version(default: str = "0.0.0") -> str:
    """
    Attempt to read the project version from pyproject.toml.

    If not found or file is missing, falls back to `default`.
    """
    pyproject = get_pyproject_path()
    if not pyproject.exists():
        return default

    try:
        text = pyproject.read_text(encoding="utf-8")
    except OSError:
        return default

    # Extremely lightweight parse; avoid extra dependencies.
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("version"):
            # version = "0.1.0"
            parts = stripped.split("=", 1)
            if len(parts) == 2:
                value = parts[1].strip().strip('"').strip("'")
                if value:
                    return value

    return default


def get_name() -> str:
    """
    Return the canonical name for this tool.
    """
    return "The Veil"


def get_codename() -> str:
    """
    Optional codename (for fun / flavor).
    """
    return "GrafanaNetes Sentinel"


def get_banner(extra: Optional[str] = None) -> str:
    """
    Render a multi-line banner used at the top of CLI invocations.

    Args:
        extra: Optional extra line to append under the main banner.

    Returns:
        str: A richly formatted ASCII banner.
    """
    name = get_name()
    codename = get_codename()
    version = get_version()

    banner = textwrap.dedent(
        f"""
        🔱 {name} — {codename}
        Version: {version}
        Timestamp: {get_timestamp()}
        Project root: {get_project_root()}
        """
    ).strip()

    if extra:
        banner = f"{banner}\n{extra.strip()}"

    return banner
