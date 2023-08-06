from pathlib import Path
from typing import Optional, List, Any, Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator

from phi.workspace.settings import WorkspaceSettings


class PhiBase(BaseModel):
    name: Optional[str] = None
    group: Optional[str] = None
    version: Optional[str] = None
    enabled: bool = True

    #  -*- Resource Control
    skip_create: bool = False
    skip_read: bool = False
    skip_update: bool = False
    skip_delete: bool = False
    recreate_on_update: bool = False
    # Skip create if resource with the same name is active
    use_cache: bool = True
    # Force create/update/delete implementation
    force: Optional[bool] = Field(None, validate_default=True)

    # -*- Debug Mode
    debug_mode: bool = False

    # -*- Resource Environment
    # Add env variables to resource where applicable
    env_vars: Optional[Dict[str, Any]] = None
    # Read env from a file in yaml format
    env_file: Optional[Path] = None
    # Add secret variables to resource where applicable
    # secrets_dict: Optional[Dict[str, Any]] = None
    # Read secrets from a file in yaml format
    secrets_file: Optional[Path] = None
    # Read secret variables from AWS Secrets
    aws_secrets: Optional[Any] = None

    # -*- Waiter Control
    wait_for_create: bool = True
    wait_for_update: bool = True
    wait_for_delete: bool = True
    waiter_delay: int = 30
    waiter_max_attempts: int = 50

    #  -*- Save to output directory
    # If True, save output to json files
    save_output: bool = False
    # The directory for the output files
    output_dir: Optional[str] = None

    #  -*- Dependencies
    depends_on: Optional[List[Any]] = None

    # -*- Workspace Settings
    workspace_settings: Optional[WorkspaceSettings] = None

    # -*- Cached Data
    cached_env_file_data: Optional[Dict[str, Any]] = None
    cached_secret_file_data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_group_name(self) -> Optional[str]:
        return self.group or self.name

    @field_validator("force", mode="before")
    def update_force(cls, force):
        if force:
            return True

        from os import getenv

        phi_cli_force = getenv("PHI_CLI_FORCE", False)
        if phi_cli_force:
            return True
        return False

    # @model_validator(mode="before")
    # def update_force(cls, data):
    #     from os import getenv
    #
    #     phi_cli_force = getenv("PHI_CLI_FORCE", False)
    #     if phi_cli_force:
    #         data["force"] = True
    #         logger.info("Setting force to True using PHI_CLI_FORCE")
    #     return data

    @property
    def workspace_root(self) -> Optional[Path]:
        return self.workspace_settings.ws_root if self.workspace_settings is not None else None

    @property
    def workspace_name(self) -> Optional[str]:
        return self.workspace_settings.ws_name if self.workspace_settings is not None else None

    @property
    def workspace_dir(self) -> Optional[Path]:
        if self.workspace_root is not None:
            workspace_dir = self.workspace_settings.workspace_dir if self.workspace_settings is not None else None
            if workspace_dir is not None:
                return self.workspace_root.joinpath(workspace_dir)
        return None

    def set_workspace_settings(self, workspace_settings: Optional[WorkspaceSettings] = None) -> None:
        if workspace_settings is not None:
            self.workspace_settings = workspace_settings

    def get_env_file_data(self) -> Optional[Dict[str, Any]]:
        if self.cached_env_file_data is None:
            from phi.utils.yaml_io import read_yaml_file

            self.cached_env_file_data = read_yaml_file(file_path=self.env_file)
        return self.cached_env_file_data

    def get_secret_file_data(self) -> Optional[Dict[str, Any]]:
        if self.cached_secret_file_data is None:
            from phi.utils.yaml_io import read_yaml_file

            self.cached_secret_file_data = read_yaml_file(file_path=self.secrets_file)
        return self.cached_secret_file_data

    def get_secret_from_file(self, secret_name: str) -> Optional[str]:
        secret_file_data = self.get_secret_file_data()
        if secret_file_data is not None:
            return secret_file_data.get(secret_name)
        return None

    def set_aws_env_vars(
        self, env_dict: Dict[str, str], aws_region: Optional[str] = None, aws_profile: Optional[str] = None
    ) -> None:
        from phi.constants import (
            AWS_REGION_ENV_VAR,
            AWS_DEFAULT_REGION_ENV_VAR,
            AWS_PROFILE_ENV_VAR,
        )

        if aws_region is not None:
            # logger.debug(f"Setting AWS Region to {aws_region}")
            env_dict[AWS_REGION_ENV_VAR] = aws_region
            env_dict[AWS_DEFAULT_REGION_ENV_VAR] = aws_region
        elif self.workspace_settings is not None and self.workspace_settings.aws_region is not None:
            # logger.debug(f"Setting AWS Region to {aws_region} using workspace_settings")
            env_dict[AWS_REGION_ENV_VAR] = self.workspace_settings.aws_region
            env_dict[AWS_DEFAULT_REGION_ENV_VAR] = self.workspace_settings.aws_region

        if aws_profile is not None:
            # logger.debug(f"Setting AWS Profile to {aws_profile}")
            env_dict[AWS_PROFILE_ENV_VAR] = aws_profile
        elif self.workspace_settings is not None and self.workspace_settings.aws_profile is not None:
            # logger.debug(f"Setting AWS Profile to {aws_profile} using workspace_settings")
            env_dict[AWS_PROFILE_ENV_VAR] = self.workspace_settings.aws_profile
