from __future__ import annotations

import json
import re
from enum import Enum
from logging import getLogger
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union

import typer
from deepdiff import DeepDiff
from pydantic import parse_obj_as

from slingshot import schemas
from slingshot.cli.shared import prompt_confirm, prompt_for_single_choice
from slingshot.schemas import ProjectManifest
from slingshot.sdk import config
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.sdk.utils import console, edit_slingshot_yaml
from slingshot.shared.utils import (
    get_data_or_raise,
    load_slingshot_project_config,
    machine_size_to_machine_type_gpu_count,
    machine_type_gpu_count_to_machine_size,
)

if TYPE_CHECKING:
    from slingshot.sdk.slingshot_sdk import SlingshotSDK

    EnvSpecPlan = tuple[
        list[tuple[schemas.EnvironmentSpec, str]],
        list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]],
        list[fragments.ExecutionEnvironmentSpec],
    ]
    AppSpecPlan = tuple[
        list[schemas.SlingshotAbstractAppSpec],
        list[tuple[schemas.SlingshotAbstractAppSpec, str]],
        list[fragments.AppSpec],
    ]
else:
    EnvSpecPlan = tuple
    AppSpecPlan = tuple

logger = getLogger(__name__)


class ApplyService:
    WAIT_FOR_ENV_POLL_INTERVAL = 2

    def __init__(self, sdk: "SlingshotSDK") -> None:
        if not (project := sdk.project):
            raise SlingshotException("No project set. Please run 'slingshot init' or 'slingshot use'.")
        self._project = project
        self._sdk = sdk

    async def plan(self, config: schemas.ProjectManifest | None = None) -> tuple[EnvSpecPlan, AppSpecPlan]:
        if not config:
            config = load_slingshot_project_config()
        env_plan, updated_env_names = await self.plan_environments(config)
        app_plan = await self.plan_apps(config, updated_env_names)
        return env_plan, app_plan

    async def plan_apps(self, config: schemas.ProjectManifest, updated_env_names: set[str]) -> AppSpecPlan:
        existing_app_specs = await self._sdk.list_apps()
        custom_apps = [app for app in config.apps if isinstance(app, schemas.SlingshotCustomAppSpec)]
        sessions = [app for app in config.apps if isinstance(app, schemas.SessionAppSpec)]
        (
            custom_app_specs_to_create,
            custom_app_specs_to_update,
            custom_app_specs_to_delete,
            custom_app_change_msgs,
        ) = _diff_existing_app_yaml_specs(existing_app_specs, custom_apps, schemas.AppType.CUSTOM, updated_env_names)
        (
            custom_session_app_specs_to_create,
            custom_session_app_specs_to_update,
            custom_session_app_specs_to_delete,
            custom_session_app_change_msgs,
        ) = _diff_existing_app_yaml_specs(
            existing_app_specs, sessions, schemas.AppType.CUSTOM, updated_env_names, schemas.AppSubType.SESSION
        )
        (
            run_specs_to_create,
            run_specs_to_update,
            run_specs_to_delete,
            run_change_msgs,
        ) = _diff_existing_app_yaml_specs(existing_app_specs, config.runs, schemas.AppType.RUN, updated_env_names)
        (
            deployment_specs_to_create,
            deployment_specs_to_update,
            deployment_specs_to_delete,
            deployment_change_msgs,
        ) = _diff_existing_app_yaml_specs(
            existing_app_specs, config.deployments, schemas.AppType.DEPLOYMENT, updated_env_names
        )

        app_specs_to_create = (
            custom_app_specs_to_create
            + custom_session_app_specs_to_create
            + run_specs_to_create
            + deployment_specs_to_create
        )
        app_specs_to_update = (
            custom_app_specs_to_update
            + custom_session_app_specs_to_update
            + run_specs_to_update
            + deployment_specs_to_update
        )
        app_specs_to_delete = (
            custom_app_specs_to_delete
            + custom_session_app_specs_to_delete
            + run_specs_to_delete
            + deployment_specs_to_delete
        )

        all_change_msgs = (
            custom_app_change_msgs + custom_session_app_change_msgs + run_change_msgs + deployment_change_msgs
        )
        if all_change_msgs:
            console.print("\n".join(all_change_msgs))

        return app_specs_to_create, app_specs_to_update, app_specs_to_delete

    async def plan_environments(self, config: schemas.ProjectManifest) -> tuple[EnvSpecPlan, set[str]]:
        existing_env_specs = await self._sdk.list_environments()
        envs_that_require_gpu = _get_envs_requiring_gpu(config)
        (
            env_specs_to_create,
            env_specs_to_update,
            env_specs_to_delete,
            updated_spec_names,
            change_msgs,
        ) = _diff_existing_env_yaml_specs(existing_env_specs, config.environments, envs_that_require_gpu)
        if change_msgs:
            console.print("\n".join(change_msgs))
        return (env_specs_to_create, env_specs_to_update, env_specs_to_delete), updated_spec_names

    async def apply_env_specs(
        self, config_: schemas.ProjectManifest, env_spec_plan: EnvSpecPlan
    ) -> tuple[list[fragments.ExecutionEnvironmentSpec], dict[str, str]]:
        env_specs_to_create, env_specs_to_update, env_specs_to_delete = env_spec_plan
        existing_specs = await self._sdk.list_environments()
        env_spec_name_to_id = {
            spec.execution_environment_spec_name: spec.execution_environment_spec_id for spec in existing_specs
        }

        envs_that_require_gpu = _get_envs_requiring_gpu(config_)
        has_env_updates = (len(env_specs_to_create) + len(env_specs_to_update) + len(env_specs_to_delete)) > 0
        if not has_env_updates:
            console.print("No changes detected to environments ✅ ")
            return [], env_spec_name_to_id

        environments_to_wait_for = []
        for spec, spec_name in env_specs_to_create:
            should_use_gpu = spec_name in envs_that_require_gpu

            try:
                new_env_spec = await self.create_env_spec(
                    environment_name=spec_name, environment_spec=spec, gpu_drivers=should_use_gpu
                )
                environments_to_wait_for.append(new_env_spec)
                env_spec_name_to_id[spec_name] = new_env_spec.execution_environment_spec_id
            except Exception as e:
                raise SlingshotException(f"Failed to create environment: {e}") from e

        for spec, existing_spec in env_specs_to_update:
            should_use_gpu = existing_spec.execution_environment_spec_name in envs_that_require_gpu
            try:
                updated_env_spec = await self.update_env_spec(
                    environment_spec=spec, existing_execution_environment_spec=existing_spec, gpu_drivers=should_use_gpu
                )
                environments_to_wait_for.append(updated_env_spec)
                spec_id = updated_env_spec.execution_environment_spec_id
                env_spec_name_to_id[existing_spec.execution_environment_spec_name] = spec_id
            except Exception as e:
                raise SlingshotException(f"Failed to update environment: {e}") from e
        for spec in env_specs_to_delete:
            try:
                await self.delete_env_spec(spec)
            except Exception as e:
                raise SlingshotException(f"Failed to delete environment: {e}") from e

        return environments_to_wait_for, env_spec_name_to_id

    async def create_env_spec(
        self, environment_name: str, environment_spec: schemas.EnvironmentSpec, gpu_drivers: bool = False
    ) -> fragments.ExecutionEnvironmentSpec:
        console.print(f"Creating environment '{environment_name}'...", end="")
        requested_python_requirements = [
            schemas.RequestedRequirement.from_str(i) for i in environment_spec.python_packages
        ]
        requested_apt_requirements = [schemas.RequestedAptPackage(name=p) for p in environment_spec.apt_packages]
        create_env_spec_resp = await self._sdk.create_environment(
            name=environment_name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            gpu_drivers=gpu_drivers,
        )
        if create_env_spec_resp.error:
            raise SlingshotException(f"Failed to create environment: {create_env_spec_resp.error}")
        console.print("✅ ")

        has_env_spec_id, is_new = get_data_or_raise(create_env_spec_resp)
        if is_new:
            logger.debug(f"Environment '{environment_name}' has changed or is new - we're building it now...")

        assert isinstance(has_env_spec_id, schemas.ExecutionEnvironmentSpecId)
        env_spec = await self._sdk.get_environment(has_env_spec_id.execution_environment_spec_id)
        assert env_spec, "Environment spec was not created"
        return env_spec

    async def update_env_spec(
        self,
        environment_spec: schemas.EnvironmentSpec,
        existing_execution_environment_spec: fragments.ExecutionEnvironmentSpec,
        gpu_drivers: bool,
    ) -> fragments.ExecutionEnvironmentSpec:
        environment_name = existing_execution_environment_spec.execution_environment_spec_name
        execution_environment_spec_id = existing_execution_environment_spec.execution_environment_spec_id
        console.print(f"Updating environment '{environment_name}'...", end="")
        requested_python_requirements = [
            schemas.RequestedRequirement.from_str(i) for i in environment_spec.python_packages
        ]
        requested_apt_requirements = [schemas.RequestedAptPackage(name=p) for p in environment_spec.apt_packages]
        await self._sdk.update_environment(
            name=environment_name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            gpu_drivers=gpu_drivers,
        )
        console.print("✅ ")
        env_spec = await self._sdk.get_environment(execution_environment_spec_id)
        assert env_spec, "Environment spec was not updated"
        return env_spec

    async def delete_env_spec(self, env_spec: fragments.ExecutionEnvironmentSpec) -> None:
        console.print(f"Deleting environment '{env_spec.execution_environment_spec_name}'...", end="")
        await self._sdk.delete_environment(environment_id=env_spec.execution_environment_spec_id)
        console.print("✅ ")

    async def _wait_for_environment(self, env_spec: fragments.ExecutionEnvironmentSpec, wait_for_s: int = 30) -> None:
        env = await self._sdk.api.get_exec_env(env_spec.execution_environment.execution_environment_id)
        assert env, "Environment not found"
        if env.build and env.build.build_status == "SUCCESS":
            # Don't show anything if it's already ready
            return
        status = env.status
        if status == schemas.ExecEnvStatus.COMPILING.value:
            console.print(f"Waiting for environment '{env_spec.execution_environment_spec_name}'.", end="")
            try:
                status = await self._sdk._wait_for_env_compile(env, max_wait=wait_for_s, should_print=True)
            except SlingshotException:
                pass

        url = await self._sdk.web_path_util.environment(env_spec)
        if status == schemas.ExecEnvStatus.COMPILING:
            console.print(f"Environment is still compiling. You might want to check back in a few minutes: {url}")
            return
        elif status == schemas.ExecEnvStatus.FAILED:
            console.print(f"Something went wrong while preparing your environment.")
            console.print(f"\n[red]Error preparing environment:[/red]{env.error_message}: {url}")
            raise typer.Exit(1)
        elif status == schemas.ExecEnvStatus.READY:
            build_ready = env.build and env.build.build_status == "SUCCESS"
            build_ready_str = "ready" if build_ready else "being built"
            console.print(f"Environment '{env_spec.execution_environment_spec_name}' is {build_ready_str}: {url}")
        else:
            raise ValueError(f"Unknown environment status: {env.status}")

    async def apply_app_specs(self, app_spec_plan: AppSpecPlan, env_spec_name_to_id: dict[str, str]) -> None:
        app_specs_to_create, app_specs_to_update, app_specs_to_delete = app_spec_plan

        has_app_updates = (len(app_specs_to_create) + len(app_specs_to_update) + len(app_specs_to_delete)) > 0
        if not has_app_updates:
            console.print("No changes detected to apps ✅ ")
            return

        for spec in app_specs_to_create:
            try:
                _ = await self.create_app_spec(app_spec=spec, exec_env_spec_id=env_spec_name_to_id[spec.environment])
            except Exception as e:
                raise SlingshotException(f"Failed to create app: {e}") from e

        for spec, spec_id in app_specs_to_update:
            try:
                await self.update_app_spec(
                    app_spec=spec, existing_app_spec_id=spec_id, exec_env_spec_id=env_spec_name_to_id[spec.environment]
                )
            except Exception as e:
                raise SlingshotException(f"Failed to update app: {e}") from e
        for spec in app_specs_to_delete:
            try:
                await self.delete_app_spec(spec)
            except Exception as e:
                raise SlingshotException(f"Failed to delete app: {e}") from e

    async def create_app_spec(
        self, app_spec: schemas.SlingshotAbstractAppSpec, exec_env_spec_id: str
    ) -> schemas.HasAppSpecId:
        console.print(f"Creating '{app_spec.name}'...", end="")
        app_type = _get_app_type(app_spec)
        app_sub_type = _get_app_sub_type(app_spec)
        machine_size = machine_type_gpu_count_to_machine_size(app_spec.machine_type, app_spec.num_gpu)
        app_spec_id_response = await self._sdk.create_app(
            name=app_spec.name,
            command=app_spec.cmd if hasattr(app_spec, "cmd") else None,
            app_type=app_type,
            app_sub_type=app_sub_type,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=app_spec.mounts,
            attach_project_credentials=(
                app_spec.attach_project_credentials if hasattr(app_spec, "attach_project_credentials") else False
            ),
            config_variables=app_spec.config_variables,
            app_port=app_spec.port if hasattr(app_spec, "port") else None,
        )
        app_spec_id = get_data_or_raise(app_spec_id_response)
        console.print("✅")
        return app_spec_id

    async def update_app_spec(
        self, app_spec: schemas.SlingshotAbstractAppSpec, existing_app_spec_id: str, exec_env_spec_id: str
    ) -> None:
        console.print(f"Updating app '{app_spec.name}'...", end="")
        machine_size = machine_type_gpu_count_to_machine_size(app_spec.machine_type, app_spec.num_gpu)
        await self._sdk.update_app(
            app_spec_id=existing_app_spec_id,
            name=app_spec.name,
            command=app_spec.cmd if hasattr(app_spec, "cmd") else None,
            env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            config_variables=app_spec.config_variables,
            mounts=app_spec.mounts,
            attach_project_credentials=(
                app_spec.attach_project_credentials if hasattr(app_spec, "attach_project_credentials") else False
            ),
            app_port=app_spec.port if hasattr(app_spec, "port") else None,
            batch_size=app_spec.batch_size if hasattr(app_spec, "batch_size") else None,
            batch_interval=app_spec.batch_interval if hasattr(app_spec, "batch_interval") else None,
        )
        console.print("✅ ")

    async def delete_app_spec(self, app_spec: fragments.AppSpec) -> None:
        console.print(f"Deleting app '{app_spec.app_spec_name}'...", end="")
        await self._sdk.delete_app(app_spec_id=app_spec.app_spec_id)
        console.print("✅ ")

    async def run(
        self,
        project_manifest: schemas.ProjectManifest,
        env_spec_plan: EnvSpecPlan,
        app_spec_plan: AppSpecPlan,
        and_wait: bool,
    ) -> list[fragments.ExecutionEnvironmentSpec]:
        """
        Returns the list of execution environment specs that were created or updated.
        """
        console.print(f"Applying 'slingshot.yaml' for project '{self._project.project_id}'.")
        env_specs_to_wait_for, env_spec_name_to_id = await self.apply_env_specs(
            project_manifest, env_spec_plan=env_spec_plan
        )
        await self.apply_app_specs(app_spec_plan=app_spec_plan, env_spec_name_to_id=env_spec_name_to_id)
        config.project_config.last_pushed_manifest = load_slingshot_project_config()
        if and_wait:
            if env_specs_to_wait_for:
                console.print("[green]Waiting for environments, you can safely exit with Ctrl+C...[/green]")
            for env in env_specs_to_wait_for:
                await self._wait_for_environment(env)
        return env_specs_to_wait_for

    async def apply_to_local(self, remote_manifest: schemas.ProjectManifest | None = None, force: bool = False) -> bool:
        """
        Applies the remote manifest to the local slingshot.yaml.

        The last pushed manifest is used as the base of the initial diff. If there is no last-pushed manifest,
        the base is an empty manifest so that all remote changes are computed in the plan and can be applied.
        Then, the local slingshot.yaml applied using the resulting diff. If there are conflicts, the user is
        prompted to override either the local or remote changes.

        Returns True if there were changes, False otherwise.
        """
        current_manifest = load_slingshot_project_config()  # Reload local, in case it was changed
        last_pushed_manifest = config.project_config.last_pushed_manifest
        is_last_pushed_manifest_empty = last_pushed_manifest is None

        diff_base = last_pushed_manifest or ProjectManifest()
        if isinstance(diff_base, ProjectManifest):
            diff_base = diff_base.dict()

        if not remote_manifest:
            remote_manifest = await remote_project_manifest(self._sdk)

        diff = DeepDiff(diff_base, remote_manifest.dict(), ignore_order=True)
        if not diff:
            logger.debug("No remote changes detected")
            return False

        console.print("[red]Conflict detected[/red]. Changes found on the remote since your last push:")
        diff_formatted = diff_to_str(diff, remote_manifest)
        diff_formatted = "\n".join([f"  [yellow]*[/yellow] {line}" for line in diff_formatted.split('\n')])
        console.print(diff_formatted)
        if not validate_if_changes_can_be_applied(diff, current_manifest=current_manifest):
            return await prompt_override_local_remote(diff=diff, remote_manifest=remote_manifest, force=force)

        console.print("[yellow]Conflict resolution[/yellow]: ", end="")
        if not (
            force
            or prompt_confirm("Do you want to apply the above changes to your local slingshot.yaml?", default=True)
        ):
            return False

        try:
            apply_to_local(diff, remote_manifest)
            # If the last pushed manifest was empty, we should set it to the remote manifest to avoid showing conflicts
            if is_last_pushed_manifest_empty:
                config.project_config.last_pushed_manifest = remote_manifest
            else:
                config.project_config.last_pushed_manifest = load_slingshot_project_config()
            return True
        except Exception as e:
            # If the validation succeeded but apply fails nonetheless, we should still prompt the user
            return await prompt_override_local_remote(diff=diff, remote_manifest=remote_manifest, force=force)

    async def plan_prompt_apply(
        self, *, force: bool, and_wait: bool = False
    ) -> tuple[bool, list[fragments.ExecutionEnvironmentSpec]]:
        """
        Plan, prompt and apply changes to the remote environment.

        If force is true, the changes will be applied without prompting. If it's a string, then only the matching
        environment spec (by ID) will be awaited.

        Returns (True, x) if any changes were applied, False otherwise. X is the list of any environment specs created
        or updated.
        """
        # We use a "last-pushed-manifest" as a merge base to determine what changes to apply.
        #  There are three cases to keep in mind:
        #  - No last-pushed-manifest and no remote manifest: it's a new project -- can safely apply the diff and push
        #  - No last-pushed-manifest and remote manifest: it's a new copy of a project -- user should pull first
        #  - last-pushed-manifest and remote manifest: it's a normal case -- perform a three-way merge
        last_pushed_manifest = config.project_config.last_pushed_manifest
        is_last_pushed_manifest_empty = last_pushed_manifest is None

        if last_pushed_manifest is None:
            last_pushed_manifest = ProjectManifest()
        if isinstance(last_pushed_manifest, ProjectManifest):
            last_pushed_manifest = last_pushed_manifest.dict()

        remote_manifest = await remote_project_manifest(self._sdk)
        remote_diff = DeepDiff(last_pushed_manifest, remote_manifest.dict(), ignore_order=True)
        if is_last_pushed_manifest_empty and len(remote_diff.keys()) > 0 and not force:
            raise SlingshotException(
                "You have unmerged remote changes. Run 'slingshot pull' and then try apply again. To ignore this "
                "error and force-apply, run 'slingshot apply -y'."
            )

        current_manifest = load_slingshot_project_config()
        if not (force or validate_if_changes_can_be_applied(remote_diff, current_manifest=current_manifest)):
            raise SlingshotException(
                "Cannot apply changes because local and remote changes conflict. Run 'slingshot pull' then try again."
            )

        any_changes_applied = False
        if not force:
            any_changes_applied = await self.apply_to_local(remote_manifest)

        manifest = load_slingshot_project_config()  # Reload local, in case it was changed
        env_spec_plan, app_spec_plan = await self.plan(config=manifest)
        if any(env_spec_plan) or any(app_spec_plan):
            if force or prompt_confirm("Do you want to apply these changes?", default=True):
                env_specs_to_wait_for = await self.run(
                    manifest, env_spec_plan=env_spec_plan, app_spec_plan=app_spec_plan, and_wait=and_wait
                )
                return True, env_specs_to_wait_for
            return any_changes_applied, []
        else:
            logger.debug("No changes detected ✅ ")
            return any_changes_applied, []


async def prompt_override_local_remote(
    diff: DeepDiff, remote_manifest: schemas.ProjectManifest, *, force: bool
) -> bool:
    unable_to_synchronise_message = (
        f"[yellow]Conflict resolution[/yellow]: Unable to synchronise remote changes to your local slingshot.yaml."
    )
    console.print(unable_to_synchronise_message)
    if not force and (
        prompt_for_single_choice("Do you want to use the local or remote version?", ["local", "remote"], default=0) == 0
    ):
        config.project_config.last_pushed_manifest = load_slingshot_project_config()
        return False

    apply_to_local(diff, remote_manifest, force=True)
    config.project_config.last_pushed_manifest = load_slingshot_project_config()
    return True


def apply_diff(local_slingshot_yaml: dict[str, Any], diff: DeepDiff, remote_manifest: schemas.ProjectManifest) -> None:
    """Applies a diff to the local slingshot.yaml, using the remote manifest as a reference."""
    for key_path, value in diff.get("values_changed", {}).items():
        keys = parse_keys(key_path)
        d = local_slingshot_yaml
        for k in keys[:-1]:
            d = d[k]  # type: ignore[index]
        new_value = value["new_value"]
        if isinstance(new_value, Enum):
            new_value = new_value.value
        if isinstance(new_value, dict):
            new_value = {k: v.value if isinstance(v, Enum) else v for k, v in new_value.items()}
        d[keys[-1]] = new_value  # type: ignore[index]
    for key_path in diff.get("dictionary_item_added", []):
        keys = parse_keys(key_path)
        d = local_slingshot_yaml
        d_ref = remote_manifest.dict()
        for k in keys[:-1]:
            d = d[k]  # type: ignore[index]
            d_ref = d_ref[k]
        d[keys[-1]] = d_ref[keys[-1]]  # type: ignore[index]
    for key_path in diff.get("dictionary_item_removed", []):
        keys = parse_keys(key_path)
        d = local_slingshot_yaml
        for k in keys[:-1]:
            d = d[k]  # type: ignore[index]
        del d[keys[-1]]  # type: ignore[arg-type]
    for key_path, value in diff.get("iterable_item_added", {}).items():
        keys = parse_keys(key_path)
        d = local_slingshot_yaml
        for k in keys[:-1]:
            d = d[k]  # type: ignore[index]
        # insert
        assert isinstance(d, list)
        if isinstance(value, dict):
            value = {k: v if not isinstance(v, Enum) else v.value for k, v in value.items()}
        d.insert(keys[-1], value)
    for key_path, value in diff.get("iterable_item_removed", {}).items():
        keys = parse_keys(key_path)
        d = local_slingshot_yaml
        for k in keys[:-1]:
            d = d[k]  # type: ignore[index]
        del d[keys[-1]]  # type: ignore[arg-type]


def parse_keys(key_path: str) -> list[Union[str, int]]:
    """
    >>> parse_keys("root['key1']['key2']")
    ['key1', 'key2']
    >>> parse_keys("root['key1'][0]['key2']")
    ['key1', 0, 'key2']
    """
    return [eval(k) for k in re.findall(r"\[([^]]+)]", key_path)]


def _key_path_to_str(key_path: str, reference: schemas.ProjectManifest) -> str:
    # e.g. root['runs'][2]['mounts'][1]['mode'] changed from 'DOWNLOAD' to 'UPLOAD'
    # extract: (runs)(2)(mounts)
    result = re.match(r"root\['(runs|apps|deployments)']\[(\d+)](.*)", key_path)
    if not result:
        key_path = key_path.replace("root", "", 1)
        rest_fields = re.findall(r"\['?([^'\]]*)'?]", key_path)
        rest_fields_str = " -> ".join(rest_fields)
        return rest_fields_str

    app_type, index, rest = result.groups()
    rest_fields = re.findall(r"\['?([^'\]]*)'?]", rest)
    rest_fields_str = " -> ".join(rest_fields)
    if rest_fields_str:
        rest_fields_str = f"-> {rest_fields_str}"
    if app_type == "runs":
        if len(reference.runs) > int(index):
            name = reference.runs[int(index)].name
            key_path = f"run '{name}' {rest_fields_str}".rstrip()
        else:
            key_path = f"run {rest_fields_str}".rstrip()

    elif app_type == "apps":
        if len(reference.apps) > int(index):
            name = reference.apps[int(index)].name
            key_path = f"app '{name}' {rest_fields_str}".rstrip()
        else:
            key_path = f"app {rest_fields_str}".rstrip()

    elif app_type == "deployments":
        if len(reference.deployments) > int(index):
            name = reference.deployments[int(index)].name
            key_path = f"deployment '{name}' {rest_fields_str}".rstrip()
        else:
            key_path = f"deployment {rest_fields_str}".rstrip()
    return key_path


def diff_to_str(diff: DeepDiff, reference: schemas.ProjectManifest) -> str:
    """Converts a diff to a human-readable string."""
    lines = []
    for key_path, value in diff.get("values_changed", {}).items():
        key_path = _key_path_to_str(key_path, reference)
        lines.append(f"{key_path} changed from '{value['old_value']}' to '{value['new_value']}'")
    for key_path in diff.get("dictionary_item_added", []):
        key_path = _key_path_to_str(key_path, reference)
        lines.append(f"{key_path} added")
    for key_path in diff.get("dictionary_item_removed", []):
        key_path = _key_path_to_str(key_path, reference)
        lines.append(f"{key_path} removed")
    for key_path, value in diff.get("iterable_item_added", {}).items():
        key_path = _key_path_to_str(key_path, reference)
        if isinstance(value, dict) and 'name' in value:
            value = value['name']
        lines.append(f"{key_path} added: \"{value}\"")
    for key_path, value in diff.get("iterable_item_removed", {}).items():
        key_path = _key_path_to_str(key_path, reference)
        if isinstance(value, dict) and 'name' in value:
            value = value['name']

        lines.append(f"{key_path} removed (was \"{value}\")")
    if set(diff.keys()) - {
        "values_changed",
        "dictionary_item_added",
        "dictionary_item_removed",
        "iterable_item_added",
        "iterable_item_removed",
    }:
        lines.append("Other changes detected, please see the diff below:")
        lines.append(str(diff))
    return "\n".join(lines)


def validate_if_changes_can_be_applied(diff: DeepDiff, current_manifest: schemas.ProjectManifest) -> bool:
    """
    Validates if the changes to reference manifest can be applied to current manifest.
    This is useful to fail early if we can't merge in the changes from the diff.
    """
    if not diff:
        return True
    if set(diff.keys()) - {
        "values_changed",
        "dictionary_item_added",
        "dictionary_item_removed",
        "iterable_item_added",
        "iterable_item_removed",
    }:
        logger.debug(f"Diff keys: {diff.keys()}")
        logger.debug(f"Unexpected changes detected, please see the diff below: {diff}")
        return False
    current_manifest = current_manifest.dict()

    for key_path, value in diff.get("values_changed", {}).items():
        keys = parse_keys(key_path)
        current_root = current_manifest
        for key in keys[:-1]:
            if isinstance(current_root, dict) and key not in current_root:
                logger.debug(f"Cannot change key that doesn't exist: {key}")
                return False
            if isinstance(current_root, list) and int(key) >= len(current_root):
                logger.debug(f"Cannot change index that doesn't exist: {key}")
                return False
            current_root = current_root[key]
        if isinstance(current_root, dict) and not keys[-1] in current_root:
            logger.debug(f"Cannot change key that doesn't exist: {keys[-1]}")
            return False
        if isinstance(current_root, list) and int(keys[-1]) >= len(current_root):
            logger.debug(f"Cannot change index that doesn't exist: {keys[-1]}")
            return False
    for key_path in diff.get("dictionary_item_added", []):
        keys = parse_keys(key_path)
        current_root = current_manifest
        for key in keys[:-1]:
            if isinstance(current_root, dict) and key not in current_root:
                logger.debug(f"Cannot add within key that doesn't exist: {key}")
                return False
            if isinstance(current_root, list) and int(key) >= len(current_root):
                logger.debug(f"Cannot add within index that doesn't exist: {key}")
                return False
            current_root = current_root[key]
        if not isinstance(current_root, dict):  # Can't add a key to a list
            logger.debug(f"Cannot add a dictionary key to a list: {current_root}")
            return False
        if keys[-1] in current_root:
            logger.debug(f"Cannot add a dictionary key that already exists: {keys[-1]}")
            return False
    for key_path in diff.get("dictionary_item_removed", []):
        keys = parse_keys(key_path)
        current_root = current_manifest
        for key in keys[:-1]:
            if isinstance(current_root, dict) and key not in current_root:
                logger.debug(f"Cannot remove within dictionary key that doesn't exist: {key}")
                return False
            current_root = current_root[key]
        if not isinstance(current_root, dict):
            logger.debug(f"Cannot remove a dictionary key from a list: {current_root}")
            return False
        if not keys[-1] in current_root:
            logger.debug(f"Cannot remove a dictionary key that doesn't exist: {keys[-1]}")
            return False  # Can't remove a key that doesn't exist
    for key_path, value in diff.get("iterable_item_added", {}).items():
        keys = parse_keys(key_path)
        current_root = current_manifest
        for key in keys[:-1]:
            if isinstance(current_root, dict) and key not in current_root:
                logger.debug(f"Cannot add iterable item within key that doesn't exist: {key}")
                return False
            current_root = current_root[key]
        if not isinstance(current_root, list):
            logger.debug(f"iterable_item_added can only be applied to lists: {current_root}")
            return False
        if value in current_root:
            logger.debug(f"Cannot add an iterable item that already exists: {value}")
            return False
    for key_path, value in diff.get("iterable_item_removed", {}).items():
        keys = parse_keys(key_path)
        current_root = current_manifest
        for key in keys[:-1]:
            if isinstance(current_root, dict) and key not in current_root:
                logger.debug(f"Cannot remove iterable item within key that doesn't exist: {key}")
                return False
            if isinstance(current_root, list) and int(key) >= len(current_root):
                logger.debug(f"Cannot remove iterable item within index that doesn't exist: {key}")
                return False
            current_root = current_root[key]
        if not isinstance(current_root, list):
            logger.debug(f"iterable_item_removed can only be applied to lists: {current_root}")
            return False
        assert isinstance((key := keys[-1]), int)  # Must be an int if we're removing an iterable item
        if len(current_root) <= key:
            logger.debug(f"Cannot remove an iterable item index that doesn't exist: {key}")
            return False
        if not current_root[key] == value:
            logger.debug(f"Cannot remove an iterable item that doesn't match the value to be removed: {value}")
            return False
    return True


def apply_to_local(diff: DeepDiff, reference_manifest: schemas.ProjectManifest, force: bool = False) -> None:
    """
    Apply a diff to the local slingshot.yaml file.
    If force, just use the reference manifest - completely ignore the local slingshot.yaml file.
    """
    if force:
        diff = DeepDiff(load_slingshot_project_config().dict(), reference_manifest.dict(), ignore_order=True)
    with edit_slingshot_yaml(raise_if_absent=True) as slingshot_yaml:
        apply_diff(slingshot_yaml, diff, reference_manifest)


def _get_app_type(spec: schemas.SlingshotAbstractAppSpec) -> schemas.AppType:
    if isinstance(spec, schemas.RunSpec):
        return schemas.AppType.RUN
    elif isinstance(spec, schemas.DeploymentSpec):
        return schemas.AppType.DEPLOYMENT
    else:
        return schemas.AppType.CUSTOM


def _get_app_sub_type(spec: schemas.SlingshotAbstractAppSpec) -> schemas.AppSubType | None:
    if isinstance(spec, schemas.SessionAppSpec):
        return schemas.AppSubType.SESSION
    return None


def _get_envs_requiring_gpu(config: schemas.ProjectManifest) -> set[str]:
    apps_runs_deployments = config.apps + config.runs + config.deployments
    envs_that_require_gpu = {app.environment for app in apps_runs_deployments if app.num_gpu and app.num_gpu > 0}
    return envs_that_require_gpu


def _diff_existing_env_yaml_specs(
    existing_env_specs: list[fragments.ExecutionEnvironmentSpec],
    yaml_env_specs: dict[str, schemas.EnvironmentSpec],
    envs_that_require_gpu: set[str],
) -> tuple[
    list[tuple[schemas.EnvironmentSpec, str]],  # tuple of spec, name
    list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]],  # tuple of spec, existing spec to update
    list[fragments.ExecutionEnvironmentSpec],  # existing specs to delete
    set[str],  # updated spec names
    list[str],  # change messages
]:
    env_specs_to_create: list[tuple[schemas.EnvironmentSpec, str]] = []
    env_specs_to_update: list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]] = []
    env_specs_to_delete: list[fragments.ExecutionEnvironmentSpec] = []

    existing_env_names = {spec.execution_environment_spec_name for spec in existing_env_specs}
    existing_env_name_to_spec = {spec.execution_environment_spec_name: spec for spec in existing_env_specs}
    yaml_env_names = {spec_name for spec_name in yaml_env_specs.keys()}

    updated_spec_names: set[str] = set()
    change_msgs: list[str] = []
    for spec_name, env_spec in yaml_env_specs.items():
        if spec_name not in existing_env_names:
            change_msgs.append(f"Detected [green]new[/green] environment '{spec_name}'")
            env_specs_to_create.append((env_spec, spec_name))
            continue

        _change_msgs: list[str] = []
        existing_env_spec = existing_env_name_to_spec[spec_name]
        should_use_gpu = spec_name in envs_that_require_gpu
        if diff := env_spec.diff(existing_env_spec, gpu_drivers=should_use_gpu):
            _change_msgs.extend(f"\t- {i}" for i in diff)
        if _change_msgs:
            change_msgs.append(f"Detected [yellow]changes[/yellow] to environment '{spec_name}'")
            change_msgs.extend(_change_msgs)
            updated_spec_names.add(spec_name)
            env_specs_to_update.append((env_spec, existing_env_spec))

    for existing_spec in existing_env_specs:
        if existing_spec.execution_environment_spec_name not in yaml_env_names:
            logger.debug(
                f"Detected environment '{existing_spec.execution_environment_spec_name}' has been [red]deleted[/red]"
            )
            logger.debug(f"\t- Environment will be [red]deleted[/red]")
            env_specs_to_delete.append(existing_spec)

    return env_specs_to_create, env_specs_to_update, env_specs_to_delete, updated_spec_names, change_msgs


def _diff_existing_app_yaml_specs(
    all_existing_app_specs: list[fragments.AppSpec],
    yaml_app_specs: list[schemas.SlingshotAbstractAppSpec],
    app_type: schemas.AppType,
    updated_env_names: set[str],
    app_sub_type: schemas.AppSubType | None = None,
) -> tuple[
    list[schemas.SlingshotAbstractAppSpec],
    list[tuple[schemas.SlingshotAbstractAppSpec, str]],
    list[fragments.AppSpec],
    list[str],
]:
    spec_display_type = "app"
    if app_type == schemas.AppType.DEPLOYMENT:
        spec_display_type = "deployment"
    elif app_type == schemas.AppType.RUN:
        spec_display_type = "run"
    if app_sub_type == schemas.AppSubType.SESSION:
        spec_display_type = "session"

    app_specs_to_create: list[schemas.SlingshotAbstractAppSpec] = []
    app_specs_to_update: list[tuple[schemas.SlingshotAbstractAppSpec, str]] = []
    app_specs_to_delete: list[fragments.AppSpec] = []

    existing_app_specs = [spec for spec in all_existing_app_specs if spec.app_type == app_type]
    existing_spec_name_to_spec: dict[str, fragments.AppSpec] = {
        app_spec.app_spec_name: app_spec for app_spec in existing_app_specs
    }
    yaml_app_spec_names = {app_spec.name for app_spec in yaml_app_specs}

    change_msgs: list[str] = []
    for app_spec in yaml_app_specs:
        if app_spec.name not in existing_spec_name_to_spec:
            change_msgs.append(f"Detected [green]new[/green] {spec_display_type} '{app_spec.name}'")
            app_specs_to_create.append(app_spec)
            continue

        existing_app_spec = existing_spec_name_to_spec[app_spec.name]
        _change_msgs: list[str] = []
        if app_spec_diff := app_spec.diff(existing_app_spec):
            _change_msgs.extend(f"\t- {i}" for i in app_spec_diff)
        if _change_msgs:
            change_msgs.append(f"Detected [yellow]changes[/yellow] to {spec_display_type} '{app_spec.name}'")
            change_msgs.extend(_change_msgs)
            if app_type in (schemas.AppType.CUSTOM, schemas.AppType.DEPLOYMENT):
                change_msgs.append(f"\t(Your {spec_display_type} will not be restarted)")

        # Only update if there are changes to the app spec itself, not just the environment
        if len(app_spec_diff) > 0:
            app_specs_to_update.append((app_spec, existing_app_spec.app_spec_id))

    for existing_app_spec in existing_app_specs:
        if (
            existing_app_spec.app_spec_name not in yaml_app_spec_names
            and existing_app_spec.app_sub_type == app_sub_type
        ):
            console.print(
                f"Detected {spec_display_type} '{existing_app_spec.app_spec_name}' has been [red]deleted[/red]"
            )
            console.print(f"\t- {spec_display_type.title()} will be [red]deleted[/red]")
            app_specs_to_delete.append(existing_app_spec)

    return app_specs_to_create, app_specs_to_update, app_specs_to_delete, change_msgs


T = TypeVar("T")
FromTo = Optional[tuple[T, T]]


def changed_str(from_to_str: FromTo[str], field: str) -> str | None:
    if from_to_str is None:
        return None
    from_str, to_str = from_to_str
    if from_str == to_str:
        return None
    return f"{field}: {from_str} -> {to_str}"


async def remote_project_manifest(sdk: "SlingshotSDK") -> schemas.ProjectManifest:
    existing_env_specs = await sdk.list_environments()
    env_specs_by_name = {
        env_spec.execution_environment_spec_name: schemas.EnvironmentSpec(
            python_packages=[
                schemas.RequestedRequirement.parse_obj(i).as_str() for i in env_spec.requested_python_requirements
            ],
            apt_packages=[schemas.RequestedAptPackage.parse_obj(i).name for i in env_spec.requested_apt_packages],
        )
        for env_spec in existing_env_specs
    }
    app_specs: list[schemas.SlingshotAbstractAppSpec] = []

    existing_app_specs = await sdk.list_apps()

    for spec in existing_app_specs:
        name = spec.app_spec_name
        environment = spec.execution_environment_spec.execution_environment_spec_name
        config_variables = json.loads(spec.config_variables) if spec.config_variables else {}
        port = spec.app_port
        attach_project_credentials = spec.service_account
        cmd = spec.app_spec_command
        machine_type, num_gpu = machine_size_to_machine_type_gpu_count(spec.machine_size)

        mounts = [
            parse_obj_as(schemas.MountSpecUnion, {"mode": i.mode, "name": i.name, "path": i.path, "tag": i.tag})
            for i in spec.mount_specs
        ]
        if spec.app_type == schemas.AppType.CUSTOM and spec.app_sub_type is None:
            app_specs.append(
                schemas.SlingshotCustomAppSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    port=port,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    mounts=mounts,
                )
            )
        elif spec.app_type == schemas.AppType.CUSTOM and spec.app_sub_type == schemas.AppSubType.SESSION:
            app_specs.append(
                schemas.SessionAppSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    using="session",
                    mounts=mounts,
                )
            )
        elif spec.app_type == schemas.AppType.RUN:
            app_specs.append(
                schemas.RunSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    mounts=mounts,
                )
            )
        elif spec.app_type == schemas.AppType.DEPLOYMENT:
            app_specs.append(
                schemas.DeploymentSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    mounts=mounts,
                )
            )
        else:
            raise ValueError(f"Unknown app type {spec.app_type}")

    return schemas.ProjectManifest(
        environments=env_specs_by_name,
        apps=[
            app
            for app in app_specs
            if isinstance(app, schemas.SlingshotCustomAppSpec) or isinstance(app, schemas.SessionAppSpec)
        ],
        runs=[app for app in app_specs if isinstance(app, schemas.RunSpec)],
        deployments=[app for app in app_specs if isinstance(app, schemas.DeploymentSpec)],
    )
