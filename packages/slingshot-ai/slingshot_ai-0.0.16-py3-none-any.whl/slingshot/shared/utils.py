from __future__ import annotations

import json
import typing
from typing import Any

from pydantic import BaseModel, ValidationError
from ruamel import yaml as r_yaml

from slingshot import schemas
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException

yaml = r_yaml.YAML()


class SlingshotFileNotFoundException(SlingshotException):
    pass


def load_slingshot_project_config() -> schemas.ProjectManifest:
    try:
        text = client_settings.slingshot_config_path.read_text()
    except FileNotFoundError as e:
        raise SlingshotFileNotFoundException(
            f"Could not find slingshot.yaml at {client_settings.slingshot_config_path}.\n"
            f"You can add one by running 'slingshot init'"
        ) from e
    try:
        d = r_yaml.safe_load(text)
    except r_yaml.YAMLError as e:
        raise SlingshotException(f"Could not parse slingshot.yaml in {client_settings.slingshot_config_path}") from e
    if not d:
        raise SlingshotException(
            f"Empty slingshot.yaml in {client_settings.slingshot_config_path}. Please run 'slingshot init'"
        )
    try:
        return schemas.ProjectManifest.parse_obj(d)
    except Exception as e:
        raise _beautify_project_manifest_parsing_exception(d, e) from e


# noinspection PyBroadException
def _beautify_project_manifest_parsing_exception(d: dict[typing.Any, typing.Any], e: Exception) -> SlingshotException:
    if (isinstance(e, ValidationError) or isinstance(e, KeyError)) and "environments" in str(e):
        for env in d["environments"].values():
            try:
                # Try to parse each environment individually to get a more helpful error message,
                #  if it's one of them that's failing.
                schemas.EnvironmentSpec.parse_obj(env)
            except ValidationError as e2:
                model = e2.model.__name__
                errs = e2.errors()
                if len(errs) > 0:
                    message = None
                    try:
                        given = errs[0]["ctx"]["given"]
                        permitted = ', '.join(list(errs[0]["ctx"]["permitted"]))
                        message = (
                            f"Invalid slingshot.yaml: [yellow]{model}[/yellow] has \"{given}\" (must be one of "
                            f"{permitted}). Contact slingshot support for assistance."
                        )
                    except Exception:
                        # If we fail to produce a valid friendly error, prefer to fall back to the generic error.
                        pass
                    if message:
                        return SlingshotException(message)

    if (isinstance(e, ValidationError) or isinstance(e, KeyError)) and "mounts" in str(e):
        for app in d.get("apps", []):
            for mount in app.get("mounts", []):
                try:
                    schemas.BaseMountSpec.parse_obj(mount)
                except ValidationError as e2:
                    try:
                        message = f"Mount for {app['name']} with {mount['path']} was invalid -- {e2.errors()[0]['msg']}"
                        return SlingshotException(message)
                    except Exception:
                        pass
                except Exception:
                    pass
        for run in d.get("runs", []):
            for mount in run.get("mounts", []):
                try:
                    schemas.BaseMountSpec.parse_obj(mount)
                except ValidationError as e2:
                    try:
                        message = f"Mount for {run['name']} with {mount['path']} was invalid -- {e2.errors()[0]['msg']}"
                        return SlingshotException(message)
                    except Exception:
                        pass
                except Exception:
                    pass
        for deployment in d.get("deployments", []):
            for mount in deployment.get("mounts", []):
                try:
                    schemas.BaseMountSpec.parse_obj(mount)
                except ValidationError as e2:
                    try:
                        message = (
                            f"Mount for {deployment['name']} with {mount['path']} was invalid -- "
                            f"{e2.errors()[0]['msg']}"
                        )
                        return SlingshotException(message)
                    except Exception:
                        pass
                except Exception:
                    pass

    if isinstance(e, SlingshotException):
        return e

    return SlingshotException(f"Invalid slingshot.yaml: {e=}")


T = typing.TypeVar("T")


class ResponseProtocol(typing.Protocol[T]):
    data: typing.Optional[T]
    error: typing.Optional[schemas.SlingshotLogicalError]


def get_data_or_raise(resp: ResponseProtocol[T]) -> T:
    if resp.error:
        raise SlingshotException(resp.error.message)
    if resp.data is None:
        raise SlingshotException("No data returned from server")
    return resp.data


_machine_size_to_machine_type_gpu_count: dict[schemas.MachineSize, tuple[schemas.MachineType, int]] = {
    schemas.MachineSize.CPU_1X: (schemas.MachineType.CPU_TINY, 0),
    schemas.MachineSize.CPU_2X: (schemas.MachineType.CPU_SMALL, 0),
    schemas.MachineSize.CPU_4X: (schemas.MachineType.CPU_MEDIUM, 0),
    schemas.MachineSize.CPU_8X: (schemas.MachineType.CPU_LARGE, 0),
    schemas.MachineSize.T4: (schemas.MachineType.T4, 1),
    schemas.MachineSize.L4: (schemas.MachineType.L4, 1),
    schemas.MachineSize.A100: (schemas.MachineType.A100, 1),
    schemas.MachineSize.A100_8X: (schemas.MachineType.A100, 8),
}

_machine_type_gpu_count_to_machine_size: dict[tuple[schemas.MachineType, int], schemas.MachineSize] = {
    v: k for k, v in _machine_size_to_machine_type_gpu_count.items()
}


def machine_size_to_machine_type_gpu_count(machine_size: schemas.MachineSize) -> tuple[schemas.MachineType, int]:
    if machine_size not in _machine_size_to_machine_type_gpu_count:
        raise ValueError(f"Unknown machine size {machine_size}")
    return _machine_size_to_machine_type_gpu_count[machine_size]


def machine_type_gpu_count_to_machine_size(machine_type: schemas.MachineType, gpu_count: int) -> schemas.MachineSize:
    if (machine_type, gpu_count) not in _machine_type_gpu_count_to_machine_size:
        raise ValueError(f"Unknown machine type {machine_type} with {gpu_count} GPUs")
    return _machine_type_gpu_count_to_machine_size[(machine_type, gpu_count)]


def pydantic_to_dict(pydantic: BaseModel, *, exclude_unset: bool = True) -> dict[str, Any]:
    # Convert enums to strings
    return json.loads(pydantic.json(exclude_none=True, exclude_unset=exclude_unset))
