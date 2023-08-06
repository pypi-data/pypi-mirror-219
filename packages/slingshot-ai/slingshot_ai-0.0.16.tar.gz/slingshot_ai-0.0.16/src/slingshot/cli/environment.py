from __future__ import annotations

from rich.table import Table

from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp

app = SlingshotCLIApp()


@app.command("list", requires_project=True)
async def list_environments(sdk: SlingshotSDK) -> None:
    """List all environments in the project."""
    envs = await sdk.list_environments()
    if not envs:
        console.print(
            "No environments found!"
            "Edit [yellow]slingshot.yaml[/yellow] or use [yellow]slingshot add[/yellow] to add an environment template."
        )
        return

    table = Table(title="Environments")
    table.add_column("Environment Name", style="cyan")
    table.add_column("Status", style="cyan")
    table.add_column("Build Status", style="cyan")
    for env in envs:
        row = [
            env.execution_environment_spec_name,
            env.execution_environment.status,
            (env.execution_environment.build and env.execution_environment.build.build_status) or "--",
        ]
        table.add_row(*row)
    console.print(table)
