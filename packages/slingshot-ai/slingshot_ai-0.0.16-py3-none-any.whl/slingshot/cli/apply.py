from __future__ import annotations

import json

import typer
from deepdiff import DeepDiff

from slingshot.cli.config.slingshot_cli import SlingshotCLIApp
from slingshot.sdk.apply import diff_to_str, remote_project_manifest
from slingshot.sdk.slingshot_sdk import SlingshotSDK
from slingshot.sdk.utils import console
from slingshot.shared.utils import load_slingshot_project_config

app = SlingshotCLIApp()


@app.command(name="apply", requires_project=True, top_level=True, requires_auth=True)
async def apply(
    *,
    sdk: SlingshotSDK,
    y: bool = typer.Option(False, "--force", "-f", help="Ignore conflicts and apply the local version to the remote"),
) -> None:
    """Apply the slingshot.yaml file to the current project

    Applies the slingshot.yaml file in the current directory to the project on Slingshot
    """
    any_changes = await sdk.apply_project(and_wait=True, force=y)
    if not any_changes:
        console.print("No changes pushed")


@app.command(name="pull", requires_project=True, top_level=True, requires_auth=True)
async def pull(
    *, sdk: SlingshotSDK, y: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation and apply changes")
) -> None:
    """Pull the slingshot.yaml file to the current project

    Pulls the slingshot.yaml file in the current directory to the project on Slingshot
    """
    any_changes_applied = await sdk.apply_to_local(force=y)
    if not any_changes_applied:
        console.print("No changes pulled")
    else:
        console.print("Changes pulled successfully")


@app.command(name="plan", requires_project=True, top_level=True, requires_auth=True, hidden=True)
async def plan(*, sdk: SlingshotSDK) -> None:
    """Plan what changes would be applied by the slingshot.yaml file, but don't apply them"""
    manifest = load_slingshot_project_config()
    remote_manifest = await remote_project_manifest(sdk)

    diff = DeepDiff(json.loads(remote_manifest.json()), json.loads(manifest.json()), ignore_order=True)
    if not diff:
        console.print("No changes detected")
    else:
        console.print(diff_to_str(diff, remote_manifest))
