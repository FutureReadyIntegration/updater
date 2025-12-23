"""
The Veil — unified CLI, updater, diagnostics, and repair toolkit.

This package is the canonical, full-featured evolution of the original Trident CLI.
It is designed to be:
- installable as a modern Python package
- runnable via `python -m veil`
- extensible with additional subcommands and backends
"""

from .identity import (
    get_project_root,
    get_timestamp,
    get_banner,
    get_version,
)

from .diagnostics import run_diagnostics
from .repair import run_repair
from .self_update import run_self_update

__all__ = [
    "get_project_root",
    "get_timestamp",
    "get_banner",
    "get_version",
    "run_diagnostics",
    "run_repair",
    "run_updater",
]

__version__ = get_version()
