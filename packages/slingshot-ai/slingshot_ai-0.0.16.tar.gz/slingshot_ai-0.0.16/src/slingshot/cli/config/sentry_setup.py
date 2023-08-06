from __future__ import annotations

import sentry_sdk
import typer

from slingshot.sdk.config import global_config
from slingshot.sdk.errors import SlingshotException
from slingshot.slingshot_version import __version__


def sentry_init() -> None:
    dsn: str | None = "https://8a6bd4ec961f4e93adf09164a5318b14@o4504169163718656.ingest.sentry.io/4505331795492864"
    if global_config.slingshot_backend_url == global_config.slingshot_local_url:
        dsn = None  # Don't send errors to Sentry when running locally

    sentry_sdk.init(dsn=dsn, traces_sample_rate=0.1, ignore_errors=[typer.Abort, typer.Exit, SlingshotException])
    sentry_sdk.set_tag("slingshot_version", __version__)
    environment = "dev" if global_config.slingshot_backend_url == global_config.slingshot_dev_url else "prod"
    sentry_sdk.set_tag("environment", environment)
