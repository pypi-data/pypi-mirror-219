from typing import Optional

import typer

from slingshot.sdk.config import global_config

from ..sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp
from .shared import prompt_for_single_choice

app = SlingshotCLIApp()


_options = ["local", "dev", "prod"]


@app.command(name="be", top_level=True, hidden=True)
async def set_backend_url(url: Optional[str] = typer.Argument(None)) -> None:
    """Set the backend URL"""
    if url is None:
        i = prompt_for_single_choice("Which backend do you want to use?", _options)
        url = _options[i]
    if url == "local":
        url = "http://localhost:8002"
    elif url == "dev":
        url = "https://dev.slingshot.xyz"
    elif url == "prod":
        url = "https://app.slingshot.xyz"
    else:
        url = url.rstrip("/")
    global_config.slingshot_backend_url = url
    console.print(f"Backend URL set to {url}")


@app.command(name="rebuild-all-environments", top_level=True, hidden=True, requires_auth=True, requires_project=False)
async def rebuild_all_environments(sdk: SlingshotSDK) -> None:
    """Invalidate the environments cache"""
    resp = await sdk.api.rebuild_all_environments()
    console.print(resp)
