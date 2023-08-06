from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseSettings, Extra


def _get_settings_json_file(settings: BaseJSONSettings) -> Path:
    if not hasattr(settings, "JSONConfig"):
        raise TypeError(f"JSONConfig not found in settings instance {settings}")
    json_config = getattr(settings, "JSONConfig")
    if not hasattr(json_config, "settings_json_file"):
        raise TypeError(f"settings_json_file not found in JSONConfig for settings instance {settings}")
    settings_json_file: Path = json_config.settings_json_file
    return settings_json_file


def _json_config_settings_source(settings: BaseJSONSettings) -> Dict[str, Any]:
    # Adapted from https://docs.pydantic.dev/usage/settings/#adding-sources
    settings_json_file = _get_settings_json_file(settings)
    if not settings_json_file.exists():
        return {}
    try:
        return json.loads(settings_json_file.read_text())
    except json.JSONDecodeError as e:
        return {}


class BaseJSONSettings(BaseSettings):
    class Config:
        @classmethod
        def customise_sources(cls, init_settings: Any, env_settings: Any, file_secret_settings: Any) -> tuple[Any, ...]:
            return init_settings, _json_config_settings_source, env_settings, file_secret_settings

        extra: Extra = Extra.allow

    def __setattr__(self, key: str, value: Any) -> None:
        if not hasattr(self, key):
            raise AttributeError(f"Cannot set attribute {key} on {self}")
        super().__setattr__(key, value)
        self._save()

    def _save(self) -> None:
        settings_json_file = _get_settings_json_file(self)
        os.makedirs(settings_json_file.parent, exist_ok=True)
        with open(settings_json_file, "w") as f:
            json.dump(self.dict(), f, indent=4)
