from __future__ import annotations

import base64
import contextlib
import copy
import hashlib
from datetime import datetime
from typing import Any, Iterator

from pydantic.tools import parse_obj_as
from rich.console import Console
from ruamel import yaml as r_yaml
from ruamel.yaml.representer import RepresenterError

from slingshot import schemas
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql.fragments import MountSpec
from slingshot.shared.utils import load_slingshot_project_config

console = Console()
yaml = r_yaml.YAML()


def time_since_string(then: datetime) -> str:
    """Compute the time since a given datetime as a pretty string"""
    now = datetime.utcnow()
    diff = now - then
    if diff.total_seconds() < 0:
        # Lol this should never happen, but it was helpful for debugging! We should remove in prod.
        return f"in the future, negative {time_since_string(now + diff)}"
    if diff.days > 0:
        return f"{diff.days} days, {diff.seconds // 3600} hours ago"
    if diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours, {diff.seconds % 3600 // 60} minutes ago"
    if diff.seconds > 60:
        return f"{diff.seconds // 60} minutes, {diff.seconds % 60} seconds ago"
    return f"{diff.seconds} seconds ago"


def bytes_to_str(num: int | float) -> str:
    """Convert bytes to a human-readable string"""
    for x in ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if num < 1024:
            if num == int(num):
                return f"{int(num)} {x}"
            return f"{num:.2f} {x}"
        num /= 1024
    return f"{num:.2f} Really Big Units"


def md5_hash(input_bytes: bytes) -> str:
    m = hashlib.md5()
    m.update(input_bytes)
    hash_digest = m.digest()
    return base64.b64encode(hash_digest).decode("utf-8")


def gql_mount_spec_to_read_mount_spec(mount_spec: MountSpec) -> schemas.MountSpecUnion:
    """Converts the MountSpec schema received from GQL type to the ReadMountSpec type."""
    return parse_obj_as(
        schemas.MountSpecUnion,
        {"path": mount_spec.path, "mode": mount_spec.mode, "tag": mount_spec.tag, "name": mount_spec.name},
    )


@contextlib.contextmanager
def edit_slingshot_yaml(raise_if_absent: bool = True) -> Iterator[dict[str, Any]]:
    if raise_if_absent:
        load_slingshot_project_config()  # For raising if absent
    text = client_settings.slingshot_config_path.read_text()
    doc = yaml.load(text)
    original = copy.deepcopy(doc)
    yield doc
    yaml.indent(mapping=2, sequence=4, offset=2)
    with client_settings.slingshot_config_path.open("w") as f:
        try:
            yaml.dump(doc, f)
        except RepresenterError as e:
            yaml.dump(original, f)
            raise SlingshotException(f"Error while editing slingshot.yaml: {e.args[0]}") from e
