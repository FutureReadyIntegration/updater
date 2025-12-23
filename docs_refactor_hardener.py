#!/usr/bin/env python3
"""
Docs Refactor – Updater → Hardener

This script:
- Walks the /docs directory
- Renames updater.md → hardener.md
- Rewrites textual references:
    "Updater"  -> "Hardener"
    "updater"  -> "hardener"
    "update"   -> "harden"   (best-effort where it makes sense)
- Creates .bak backups before modifying any file
- Skips obvious binary assets
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parent
DOCS_ROOT = PROJECT_ROOT / "docs"

SKIP_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico",
    ".svg", ".ttf", ".woff", ".woff2", ".pdf",
}


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    # heuristic: small read to see if it looks like text
    try:
        with path.open("rb") as f:
            chunk = f.read(2048)
        chunk.decode("utf-8")
        return True
    except Exception:
        return False


def iter_docs_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file() and is_text_file(p):
            yield p


def backup_once(path: Path):
    bak = path.with_suffix(path.suffix + ".bak")
    if bak.exists():
        return
    bak.write_bytes(path.read_bytes())
    print(f"[BACKUP] {path} -> {bak}")


def rewrite_content(text: str) -> str:
    """
    Apply ordered replacements to avoid collisions.
    Adjust/extend these as needed.
    """
    # Whole-word / capitalized forms first
    replacements = [
        ("Veil Updater", "Veil Sentinel Hardener"),
        ("Updater Module", "Hardener Module"),
        ("updater module", "hardener module"),

        ("Updater", "Hardener"),
        ("updater", "hardener"),

        # Action verbs – this is a bit heuristic
        ("run the updater", "run the hardener"),
        ("Run the updater", "Run the hardener"),
        ("update pass", "hardening pass"),
        ("update pipeline", "hardening pipeline"),
        ("Update pipeline", "Hardening pipeline"),

        # Generic verb-ish swaps (careful: very broad)
        ("update run", "hardener run"),
        ("update", "harden"),
        ("Update", "Harden"),
    ]

    new = text
    for old, new_val in replacements:
        new = new.replace(old, new_val)
    return new


def process_file(path: Path):
    original = path.read_text(encoding="utf-8")
    transformed = rewrite_content(original)
    if transformed == original:
        print(f"[SKIP] {path}: no changes")
        return

    backup_once(path)
    path.write_text(transformed, encoding="utf-8")
    print(f"[WRITE] {path}")


def maybe_rename_updater_md():
    old = DOCS_ROOT / "updater.md"
    new = DOCS_ROOT / "hardener.md"
    if old.exists():
        if new.exists():
            print(f"[WARN] {new} already exists; not renaming {old}")
            return
        old.rename(new)
        print(f"[RENAME] {old} -> {new}")


def main():
    if not DOCS_ROOT.exists():
        print(f"[ERROR] docs directory not found at {DOCS_ROOT}")
        return

    print("🔱 Starting docs refactor: Updater → Hardener")

    maybe_rename_updater_md()

    for path in iter_docs_files(DOCS_ROOT):
        process_file(path)

    print("🔱 Docs refactor complete")


if __name__ == "__main__":
    main()
