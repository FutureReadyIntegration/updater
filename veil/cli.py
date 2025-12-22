from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from .diagnostics import run_diagnostics, render_diagnostics_report
from .repair import run_repair
from .updater import run_updater
from .identity import get_banner
from .logging import log


def _print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def _handle_diagnostics(args: argparse.Namespace) -> None:
    result = run_diagnostics()
    if args.json:
        _print_json(result)
    else:
        print(get_banner(extra="Mode: diagnostics"))
        print()
        print(render_diagnostics_report(result))


def _handle_repair(args: argparse.Namespace) -> None:
    result = run_repair()
    if args.json:
        _print_json(result)
    else:
        print(get_banner(extra="Mode: repair"))
        print()
        print(json.dumps(result, indent=2, sort_keys=True))


def _handle_update(args: argparse.Namespace, apply_changes: bool) -> None:
    result = run_updater(dry_run=not apply_changes)
    mode = "update-apply" if apply_changes else "update (dry run)"

    if args.json:
        _print_json(result)
    else:
        print(get_banner(extra=f"Mode: {mode}"))
        print()
        print(json.dumps(result, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veil",
        description="🔱 The Veil — Unified CLI for diagnostics, repair, and updates.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of human-readable text.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # diagnostics
    diag_parser = subparsers.add_parser(
        "diagnostics",
        help="Run diagnostics checks and report environment health.",
    )
    diag_parser.set_defaults(func=_handle_diagnostics)

    # repair
    repair_parser = subparsers.add_parser(
        "repair",
        help="Run repair routines to fix common issues.",
    )
    repair_parser.set_defaults(func=_handle_repair)

    # update (dry run)
    update_parser = subparsers.add_parser(
        "update",
        help="Run updater in dry-run mode (diff only, no writes).",
    )
    update_parser.set_defaults(func=lambda args: _handle_update(args, apply_changes=False))

    # update-apply
    update_apply_parser = subparsers.add_parser(
        "update-apply",
        help="Run updater and apply changes (with backups).",
    )
    update_apply_parser.set_defaults(func=lambda args: _handle_update(args, apply_changes=True))

    return parser

    # self-update
    self_update_parser = subparsers.add_parser(
    "self-update",
    help="Check for the latest version and optionally update The Veil."
    )
    self_update_parser.add_argument(
    "--apply",
    action="store_true",
    help="Apply the update if a newer version is available."
    )
    self_update_parser.set_defaults(func=_handle_self_update)

def _handle_self_update(args: argparse.Namespace) -> None:
    from .self_update import run_self_update

    result = run_self_update(apply=args.apply)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(get_banner(extra="Mode: self-update"))
        print()
        print(json.dumps(result, indent=2, sort_keys=True))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    log("CLI invoked", context={"command": args.command, "json": bool(getattr(args, "json", False))})

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return

    func(args)
