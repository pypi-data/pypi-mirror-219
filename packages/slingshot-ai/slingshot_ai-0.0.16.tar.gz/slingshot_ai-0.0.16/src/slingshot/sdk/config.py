from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings, validator

from .. import schemas
from .config_utils import BaseJSONSettings

"""
We have three types of settings:
- ClientSettings just state defaults for where to store stuff on the client's machine
- LocalConfig is the local config file for a specific project. This may include the project id or anything cached from
recent API calls.
- GlobalConfig is the global config file for the user. This may include auth info, etc.
"""


class ClientSettings(BaseSettings):
    """Settings for the client"""

    project_config_folder = Path(os.getcwd()) / ".slingshot"
    global_config_folder = Path.home() / ".slingshot"
    slingshot_config_filename = "slingshot.yaml"
    slingshot_config_path = Path(os.getcwd()) / slingshot_config_filename


client_settings = ClientSettings()


class GlobalConfig(BaseJSONSettings):
    slingshot_local_url = "http://localhost:8002"
    slingshot_dev_url = "https://dev.slingshot.xyz"
    slingshot_prod_url = "https://app.slingshot.xyz"
    slingshot_backend_url = slingshot_prod_url  # rstrip("/") is called on this
    hasura_admin_secret: Optional[str] = None
    auth_token: Optional[schemas.AuthTokenUnion] = None
    check_for_updates_interval: float = 60 * 60 * 1  # 1 hour
    last_checked_for_updates: Optional[float] = None

    @validator("slingshot_backend_url")
    def slingshot_backend_url_strip_slash(cls, v: str) -> str:
        # If a backend is set in global_config, use that instead of the default or env var
        v = v.rstrip("/")
        return v

    class JSONConfig:
        settings_json_file: Path = client_settings.global_config_folder / "config.json"


class ProjectConfig(BaseJSONSettings):
    project_id: Optional[str] = None
    last_pushed_manifest: Optional[dict[str, Any]] = None

    class JSONConfig:
        settings_json_file: Path = client_settings.project_config_folder / "config.json"


global_config = GlobalConfig()
project_config = ProjectConfig()
