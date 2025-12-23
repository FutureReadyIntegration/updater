from __future__ import annotations

import json
import typer
from rich.console import Console
from rich.panel import Panel
from rich import box

from trident.core.self_update import run_self_update
from trident.core.config import set_default_channel, get_default_channel
from trident.core.channel import validate_channel

app = typer.Typer(add_completion=False)
console = Console()


# ------------------------------------------------------------
# Global Options (JSON mode)
# ------------------------------------------------------------
@app.callback()
def main(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output results in JSON format."
    )
):
    typer.get_current_context().obj = {"json": json_output}


# ------------------------------------------------------------
# UPDATE (dry-run)
# ------------------------------------------------------------
@app.command(name="update")
def update_dry_run(
    channel: str = typer.Option(
        None,
        "--channel",
        help="Choose update channel: stable, edge, dev. If omitted, uses default.",
    )
):
    """
    Check for updates without applying them.
    """
    ctx = typer.get_current_context()
    as_json = ctx.obj.get("json", False)

    result = run_self_update(apply=False, channel=channel)

    if as_json:
        console.print(json.dumps(result, indent=2))
        return

    console.print(
        Panel.fit(
            f"Update Check (channel: {result.get('channel')})",
            style="bold yellow",
            box=box.ROUNDED,
        )
    )

    for key, value in result.items():
        console.print(f"[cyan]{key}[/cyan]: {value}")


# ------------------------------------------------------------
# UPDATE-APPLY
# ------------------------------------------------------------
@app.command(name="update-apply")
def update_apply(
    channel: str = typer.Option(
        None,
        "--channel",
        help="Choose update channel: stable, edge, dev. If omitted, uses default.",
    )
):
    """
    Apply an update using the selected release channel.
    """
    ctx = typer.get_current_context()
    as_json = ctx.obj.get("json", False)

    result = run_self_update(apply=True, channel=channel)

    if as_json:
        console.print(json.dumps(result, indent=2))
        return

    title = (
        f"Update Applied (channel: {result.get('channel')})"
        if result.get("applied")
        else f"Update Failed (channel: {result.get('channel')})"
    )

    panel_style = "bold green" if result.get("applied") else "bold red"

    console.print(
        Panel.fit(
            title,
            style=panel_style,
            box=box.ROUNDED,
        )
    )

    for key, value in result.items():
        console.print(f"[cyan]{key}[/cyan]: {value}")


# ------------------------------------------------------------
# PROMOTE VERSION → CHANNEL
# ------------------------------------------------------------
@app.command(name="promote")
def promote_version(
    version: str = typer.Argument(..., help="Version to promote, e.g. 1.1.3"),
    to: str = typer.Option(
        "stable",
        "--to",
        help="Channel to promote to: stable, edge, dev.",
    ),
):
    """
    Promote a versioned updater image to a rolling channel.
    """
    import subprocess

    ctx = typer.get_current_context()
    as_json = ctx.obj.get("json", False)

    # Validate channel
    channel = validate_channel(to)

    source_image = f"notchofhwend/updater:{version}"
    target_image = f"notchofhwend/updater:{channel}"

    result = {
        "version": version,
        "channel": channel,
        "source_image": source_image,
        "target_image": target_image,
        "promoted": False,
    }

    try:
        subprocess.check_call(["docker", "pull", source_image])
        subprocess.check_call(["docker", "tag", source_image, target_image])
        subprocess.check_call(["docker", "push", target_image])
        result["promoted"] = True

    except Exception as exc:
        result["error"] = str(exc)

    if as_json:
        console.print(json.dumps(result, indent=2))
        return

    title = (
        f"Promoted {version} → {channel}"
        if result["promoted"]
        else f"Promotion Failed ({version} → {channel})"
    )
    style = "bold green" if result["promoted"] else "bold red"

    console.print(Panel.fit(title, style=style, box=box.ROUNDED))

    for key, value in result.items():
        console.print(f"[cyan]{key}[/cyan]: {value}")


# ------------------------------------------------------------
# SET DEFAULT CHANNEL
# ------------------------------------------------------------
@app.command(name="set-channel")
def set_channel(
    channel: str = typer.Argument(..., help="Channel to set as default: stable, edge, dev.")
):
    """
    Set the default update channel for this machine.
    """
    ctx = typer.get_current_context()
    as_json = ctx.obj.get("json", False)

    result = set_default_channel(channel)

    if as_json:
        console.print(json.dumps(result, indent=2))
        return

    console.print(
        Panel.fit(
            f"Default channel set to: {result['channel']}",
            style="bold green",
            box=box.ROUNDED,
        )
    )


# ------------------------------------------------------------
# SHOW CURRENT CONFIG
# ------------------------------------------------------------
@app.command(name="status")
def status():
    """
    Show updater status and default channel.
    """
    ctx = typer.get_current_context()
    as_json = ctx.obj.get("json", False)

    default_channel = get_default_channel()

    result = {
        "default_channel": default_channel,
    }

    if as_json:
        console.print(json.dumps(result, indent=2))
        return

    console.print(
        Panel.fit(
            f"Default Channel: {default_channel}",
            style="bold cyan",
            box=box.ROUNDED,
        )
    )


# ------------------------------------------------------------
# ENTRYPOINT
# ------------------------------------------------------------
def main_entry():
    app()


if __name__ == "__main__":
    main_entry()
