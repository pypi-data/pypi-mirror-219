from __future__ import annotations

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for the CLI"""

    auth0_timeout_sec: int = 300


settings = Settings()
