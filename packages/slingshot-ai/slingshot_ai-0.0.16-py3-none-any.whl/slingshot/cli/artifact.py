from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.table import Table

from ..sdk.errors import SlingshotException
from ..sdk.graphql import fragments
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp
from .shared import bytes_to_human_readable_size, datetime_to_human_readable, prompt_for_single_choice

MAX_ARTIFACTS_TO_SHOW = 20

app = SlingshotCLIApp()


@app.command(name="upload", requires_project=True)
async def upload_artifact(
    file_path: Path = typer.Argument(..., help="Path to file to upload"),
    artifact_tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Artifact tag"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Upload blob artifact."""
    artifact = await sdk.upload_artifact(artifact_path=file_path, blob_artifact_tag=artifact_tag)
    if not artifact:
        raise SlingshotException(f"Failed to upload artifact: {file_path}")
    web_path_to_artifact = await sdk.web_path_util.blob_artifact(artifact)
    console.print(f"Created blob artifact: [link={web_path_to_artifact}]{artifact.name}[/link]")


def _show_artifacts_table(artifacts: list[fragments.BlobArtifact]) -> None:
    table = Table(title="Artifacts")
    table.add_column("Artifact Name", style="cyan")
    table.add_column("Tag", style="cyan")
    table.add_column("Bytes Size", style="cyan")
    table.add_column("Created At", style="cyan")
    table.add_column("Provenance", style="cyan")

    for blob_artifact in artifacts:
        upload_mount = blob_artifact.origin_mount
        provenance = (
            upload_mount
            and (
                # TODO: fetch the deep link to the deployment and provide a link to it by human-friendly name and URI.
                (upload_mount.deployment_id and f"Deployment {upload_mount.deployment_id} ({upload_mount.mount_path})")
                or (upload_mount.run_id and f"Run {upload_mount.run_id} ({upload_mount.mount_path})")
            )
            or "Upload"
        )
        rows = [
            blob_artifact.name,
            blob_artifact.tag,
            bytes_to_human_readable_size(blob_artifact.bytes_size),
            datetime_to_human_readable(blob_artifact.created_at),
            provenance,
        ]
        table.add_row(*rows)
    console.print(table)


@app.command(name="list", requires_project=True)
async def list_artifacts(
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Artifact tag"),
    *,
    sdk: SlingshotSDK,
    show_system: bool = typer.Option(False, "--system", "-s", help="Show system artifacts"),
    all_: bool = typer.Option(False, "--all", "-a", help="Show all artifacts and more details"),
) -> None:
    """List blob artifacts.

    If --tag is provided, only blob artifacts with the matching tag will be returned.

    By default, only user-generated artifacts are shown. To show system artifacts (code/upsert), use --system.
    """
    artifacts = await sdk.list_artifacts(tag=tag)  # TODO: Paginate in SDK, not CLI
    if not artifacts:
        raise SlingshotException("No artifacts found.")

    if not show_system:
        artifacts = [a for a in artifacts if not a.tag == "code" and not a.tag == "upsert"]

    artifacts_ = artifacts if all_ else artifacts[:MAX_ARTIFACTS_TO_SHOW]
    _show_artifacts_table(artifacts_)
    if not all_ and len(artifacts) > len(artifacts_):
        console.print(f"Showing {len(artifacts_)} of {len(artifacts)} artifacts. Use --all to show all.")


@app.command(name="download", requires_project=True)
async def download_artifact(
    name: Optional[str] = typer.Argument(None, help="Artifact name"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Artifact tag"),
    output_filename_: Optional[str] = typer.Option(None, "--output", "-o", help="Filename to save model to"),
    get_latest: bool = typer.Option(False, "--latest", "-l", help="Get latest artifact"),
    unzip: bool = typer.Option(False, "--unzip", "-u", help="Unzip the artifact when downloading"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Download blob artifact.
    If --tag is provided, only blob artifacts matching the tag will be shown
    If --latest is passed, the latest artifact that matches the tag (if provided) will be downloaded
    """
    if name is not None and tag is not None:
        raise typer.BadParameter("Must provide either --tag or artifact name, not both")

    if name is None:
        artifacts = await sdk.list_artifacts(tag=tag)
        if not artifacts:
            raise SlingshotException("No artifacts found")

        if get_latest:
            artifact_id = artifacts[0].blob_artifact_id
        else:
            # Prompt user to select artifact
            artifact_display_names = [f"{a.name} ({a.tag})" if a.tag else a.name for a in artifacts]
            index = prompt_for_single_choice(
                "Select an artifact to download", artifact_display_names, skip_if_one_value=True
            )
            artifact_id = artifacts[index].blob_artifact_id
    else:
        blob_artifact = await sdk.get_artifact(name)
        if not blob_artifact:
            raise SlingshotException(f"Could not find artifact '{name}'")
        artifact_id = blob_artifact.blob_artifact_id

    save_filename = await sdk.download_artifact(
        artifact_id, save_path=output_filename_, prompt_overwrite=True, unzip=unzip
    )
    console.print(f"Artifact saved to {save_filename}")


@app.command(name="upsert", requires_project=True)
async def upsert_dataset_artifact(
    dataset_tag: str = typer.Argument(..., help="Base artifact tag which contains the dataset"),
    upsert_file: Path = typer.Argument(..., help="Path to upsert file to apply to the dataset"),
    *,
    sdk: SlingshotSDK,
) -> None:
    await sdk.upsert_dataset_artifact(upsert_file, dataset_tag=dataset_tag)
