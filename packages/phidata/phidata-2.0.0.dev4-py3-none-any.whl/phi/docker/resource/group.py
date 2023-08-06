from typing import List, Optional

from phi.docker.app.base import DockerApp
from phi.docker.app.context import DockerBuildContext
from phi.docker.api_client import DockerApiClient
from phi.docker.resource.base import DockerResource
from phi.infra.resource.group import InfraResourceGroup
from phi.workspace.settings import WorkspaceSettings
from phi.utils.log import logger


class DockerResourceGroup(InfraResourceGroup):
    network: str = "bridge"
    # URL for the Docker server. For example, unix:///var/run/docker.sock or tcp://127.0.0.1:1234
    base_url: Optional[str] = None

    apps: Optional[List[DockerApp]] = None
    resources: Optional[List[DockerResource]] = None

    # -*- Cached Data
    _api_client: Optional[DockerApiClient] = None

    @property
    def docker_client(self) -> DockerApiClient:
        if self._api_client is None:
            self._api_client = DockerApiClient(base_url=self.base_url)
        return self._api_client

    def create_resources(
        self,
        group_filter: Optional[str] = None,
        name_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        dry_run: Optional[bool] = False,
        auto_confirm: Optional[bool] = False,
        force: Optional[bool] = None,
        workspace_settings: Optional[WorkspaceSettings] = None,
    ):
        from phi.cli.console import print_info, print_heading, confirm_yes_no
        from phi.docker.resource.types import DockerContainer, DockerResourceInstallOrder

        logger.debug("-*- Creating DockerResources")
        # Build a list of DockerResources to create
        resources_to_create: List[DockerResource] = []
        if self.resources is not None:
            for r in self.resources:
                if r.should_create(
                    group_filter=group_filter,
                    name_filter=name_filter,
                    type_filter=type_filter,
                ):
                    r.set_workspace_settings(workspace_settings=workspace_settings)
                    resources_to_create.append(r)

        # Build a list of DockerApps to create
        apps_to_create: List[DockerApp] = []
        if self.apps is not None:
            for app in self.apps:
                if app.should_create(group_filter=group_filter):
                    apps_to_create.append(app)

        # Get the list of DockerResources from the DockerApps
        if len(apps_to_create) > 0:
            logger.debug(f"Found {len(apps_to_create)} apps to create")
            for app in apps_to_create:
                app.set_workspace_settings(workspace_settings=workspace_settings)
                app_resources = app.get_resources(build_context=DockerBuildContext(network=self.network))
                if len(app_resources) > 0:
                    for app_resource in app_resources:
                        if isinstance(app_resource, DockerResource) and app_resource.should_create(
                            name_filter=name_filter, type_filter=type_filter
                        ):
                            resources_to_create.append(app_resource)

        # Sort the DockerResources in install order
        resources_to_create.sort(key=lambda x: DockerResourceInstallOrder.get(x.__class__.__name__, 5000))

        # Deduplicate DockerResources
        deduped_resources_to_create: List[DockerResource] = []
        for r in resources_to_create:
            if r not in deduped_resources_to_create:
                deduped_resources_to_create.append(r)

        # Implement dependency sorting
        final_docker_resources: List[DockerResource] = []
        logger.debug("-*- Building DockerResources dependency graph")
        for docker_resource in deduped_resources_to_create:
            # Logic to follow if resource has dependencies
            if docker_resource.depends_on is not None:
                # Add the dependencies before the resource itself
                for dep in docker_resource.depends_on:
                    if isinstance(dep, DockerResource):
                        if dep not in final_docker_resources:
                            logger.debug(f"-*- Adding {dep.name}, dependency of {docker_resource.name}")
                            final_docker_resources.append(dep)

                # Add the resource to be created after its dependencies
                if docker_resource not in final_docker_resources:
                    logger.debug(f"-*- Adding {docker_resource.name}")
                    final_docker_resources.append(docker_resource)
            else:
                # Add the resource to be created if it has no dependencies
                if docker_resource not in final_docker_resources:
                    logger.debug(f"-*- Adding {docker_resource.name}")
                    final_docker_resources.append(docker_resource)

        # Track the total number of DockerResources to create for validation
        num_resources_to_create: int = len(final_docker_resources)
        num_resources_created: int = 0
        if num_resources_to_create == 0:
            print_info("No DockerResources to create")
            return

        if dry_run:
            print_heading("--**- Docker resources to create:")
            for resource in final_docker_resources:
                print_info(f"  -+-> {resource.get_resource_type()}: {resource.get_resource_name()}")
            print_info(f"\nNetwork: {self.network}")
            print_info(f"Total {num_resources_to_create} resources")
            return

        # Validate resources to be created
        if not auto_confirm:
            print_heading("--**-- Confirm resources to create:")
            for resource in final_docker_resources:
                print_info(f"  -+-> {resource.get_resource_type()}: {resource.get_resource_name()}")
            print_info(f"\nNetwork: {self.network}")
            print_info(f"Total {num_resources_to_create} resources")
            confirm = confirm_yes_no("\nConfirm deploy")
            if not confirm:
                print_info("-*-")
                print_info("-*- Skipping deploy")
                print_info("-*-")
                exit(0)

        for resource in final_docker_resources:
            print_info(f"\n-==+==- {resource.get_resource_type()}: {resource.get_resource_name()}")
            if force is True:
                resource.force = True
            if isinstance(resource, DockerContainer):
                if resource.network is None and self.network is not None:
                    resource.network = self.network
            # logger.debug(resource)
            try:
                _resource_created = resource.create(docker_client=self.docker_client)
                if _resource_created:
                    num_resources_created += 1
                else:
                    if workspace_settings is not None and not workspace_settings.continue_on_create_failure:
                        return False
            except Exception as e:
                logger.error(f"Failed to create {resource.get_resource_type()}: {resource.get_resource_name()}")
                logger.error(e)
                logger.error("Please fix and try again...")

        print_info(f"\n# Resources created: {num_resources_created}/{num_resources_to_create}")
        if num_resources_to_create == num_resources_created:
            return True

        logger.error(
            f"Resources created: {num_resources_created} do not match resources required: {num_resources_to_create}"  # noqa: E501
        )
        return False

    def delete_resources(
        self,
        group_filter: Optional[str] = None,
        name_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        dry_run: Optional[bool] = False,
        auto_confirm: Optional[bool] = False,
        force: Optional[bool] = None,
        workspace_settings: Optional[WorkspaceSettings] = None,
    ):
        from phi.cli.console import print_info, print_heading, confirm_yes_no
        from phi.docker.resource.types import DockerContainer, DockerResourceInstallOrder

        logger.debug("-*- Deleting DockerResources")
        # Build a list of DockerResources to delete
        resources_to_delete: List[DockerResource] = []
        if self.resources is not None:
            for r in self.resources:
                if r.should_delete(
                    group_filter=group_filter,
                    name_filter=name_filter,
                    type_filter=type_filter,
                ):
                    r.set_workspace_settings(workspace_settings=workspace_settings)
                    resources_to_delete.append(r)

        # Build a list of DockerApps to delete
        apps_to_delete: List[DockerApp] = []
        if self.apps is not None:
            for app in self.apps:
                if app.should_delete(group_filter=group_filter):
                    apps_to_delete.append(app)

        # Get the list of DockerResources from the DockerApps
        if len(apps_to_delete) > 0:
            logger.debug(f"Found {len(apps_to_delete)} apps to delete")
            for app in apps_to_delete:
                app.set_workspace_settings(workspace_settings=workspace_settings)
                app_resources = app.get_resources(build_context=DockerBuildContext(network=self.network))
                if len(app_resources) > 0:
                    for app_resource in app_resources:
                        if isinstance(app_resource, DockerResource) and app_resource.should_delete(
                            name_filter=name_filter, type_filter=type_filter
                        ):
                            resources_to_delete.append(app_resource)

        # Sort the DockerResources in install order
        resources_to_delete.sort(key=lambda x: DockerResourceInstallOrder.get(x.__class__.__name__, 5000), reverse=True)

        # Deduplicate DockerResources
        deduped_resources_to_delete: List[DockerResource] = []
        for r in resources_to_delete:
            if r not in deduped_resources_to_delete:
                deduped_resources_to_delete.append(r)

        # Implement dependency sorting
        final_docker_resources: List[DockerResource] = []
        logger.debug("-*- Building DockerResources dependency graph")
        for docker_resource in deduped_resources_to_delete:
            # Logic to follow if resource has dependencies
            if docker_resource.depends_on is not None:
                # 1. Reverse the order of dependencies
                docker_resource.depends_on.reverse()

                # 2. Remove the dependencies if they are already added to the final_docker_resources
                for dep in docker_resource.depends_on:
                    if dep in final_docker_resources:
                        logger.debug(f"-*- Removing {dep.name}, dependency of {docker_resource.name}")
                        final_docker_resources.remove(dep)

                # 3. Add the resource to be deleted before its dependencies
                if docker_resource not in final_docker_resources:
                    logger.debug(f"-*- Adding {docker_resource.name}")
                    final_docker_resources.append(docker_resource)

                # 4. Add the dependencies back in reverse order
                for dep in docker_resource.depends_on:
                    if isinstance(dep, DockerResource):
                        if dep not in final_docker_resources:
                            logger.debug(f"-*- Adding {dep.name}, dependency of {docker_resource.name}")
                            final_docker_resources.append(dep)
            else:
                # Add the resource to be deleted if it has no dependencies
                if docker_resource not in final_docker_resources:
                    logger.debug(f"-*- Adding {docker_resource.name}")
                    final_docker_resources.append(docker_resource)

        # Track the total number of DockerResources to delete for validation
        num_resources_to_delete: int = len(final_docker_resources)
        num_resources_deleted: int = 0
        if num_resources_to_delete == 0:
            print_info("No DockerResources to delete")
            return

        if dry_run:
            print_heading("--**- Docker resources to delete:")
            for resource in final_docker_resources:
                print_info(f"  -+-> {resource.get_resource_type()}: {resource.get_resource_name()}")
            print_info(f"\nNetwork: {self.network}")
            print_info(f"Total {num_resources_to_delete} resources")
            return

        # Validate resources to be deleted
        if not auto_confirm:
            print_heading("--**-- Confirm resources to delete:")
            for resource in final_docker_resources:
                print_info(f"  -+-> {resource.get_resource_type()}: {resource.get_resource_name()}")
            print_info(f"\nNetwork: {self.network}")
            print_info(f"Total {num_resources_to_delete} resources")
            confirm = confirm_yes_no("\nConfirm delete")
            if not confirm:
                print_info("-*-")
                print_info("-*- Skipping delete")
                print_info("-*-")
                exit(0)

        for resource in final_docker_resources:
            print_info(f"\n-==+==- {resource.get_resource_type()}: {resource.get_resource_name()}")
            if force is True:
                resource.force = True
            if isinstance(resource, DockerContainer):
                if resource.network is None and self.network is not None:
                    resource.network = self.network
            # logger.debug(resource)
            try:
                _resource_deleted = resource.delete(docker_client=self.docker_client)
                if _resource_deleted:
                    num_resources_deleted += 1
                else:
                    if workspace_settings is not None and not workspace_settings.continue_on_delete_failure:
                        return False
            except Exception as e:
                logger.error(f"Failed to delete {resource.get_resource_type()}: {resource.get_resource_name()}")
                logger.error(e)
                logger.error("Please fix and try again...")

        print_info(f"\n# Resources deleted: {num_resources_deleted}/{num_resources_to_delete}")
        if num_resources_to_delete == num_resources_deleted:
            return True

        logger.error(
            f"Resources deleted: {num_resources_deleted} do not match resources required: {num_resources_to_delete}"  # noqa: E501
        )
        return False

    def update_resources(
        self,
        group_filter: Optional[str] = None,
        name_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        dry_run: Optional[bool] = False,
        auto_confirm: Optional[bool] = False,
        force: Optional[bool] = None,
        workspace_settings: Optional[WorkspaceSettings] = None,
    ):
        from phi.cli.console import print_info, print_heading, confirm_yes_no
        from phi.docker.resource.types import DockerContainer, DockerResourceInstallOrder

        logger.debug("-*- Updating DockerResources")

        # Build a list of DockerResources to update
        resources_to_update: List[DockerResource] = []
        if self.resources is not None:
            for r in self.resources:
                if r.should_update(
                    group_filter=group_filter,
                    name_filter=name_filter,
                    type_filter=type_filter,
                ):
                    r.set_workspace_settings(workspace_settings=workspace_settings)
                    resources_to_update.append(r)

        # Build a list of DockerApps to update
        apps_to_update: List[DockerApp] = []
        if self.apps is not None:
            for app in self.apps:
                if app.should_update(group_filter=group_filter):
                    apps_to_update.append(app)

        # Get the list of DockerResources from the DockerApps
        if len(apps_to_update) > 0:
            logger.debug(f"Found {len(apps_to_update)} apps to update")
            for app in apps_to_update:
                app.set_workspace_settings(workspace_settings=workspace_settings)
                app_resources = app.get_resources(build_context=DockerBuildContext(network=self.network))
                if len(app_resources) > 0:
                    for app_resource in app_resources:
                        if isinstance(app_resource, DockerResource) and app_resource.should_update(
                            name_filter=name_filter, type_filter=type_filter
                        ):
                            resources_to_update.append(app_resource)

        # Sort the DockerResources in install order
        resources_to_update.sort(key=lambda x: DockerResourceInstallOrder.get(x.__class__.__name__, 5000), reverse=True)

        # Deduplicate DockerResources
        deduped_resources_to_update: List[DockerResource] = []
        for r in resources_to_update:
            if r not in deduped_resources_to_update:
                deduped_resources_to_update.append(r)

        # Implement dependency sorting
        final_docker_resources: List[DockerResource] = []
        logger.debug("-*- Building DockerResources dependency graph")
        for docker_resource in deduped_resources_to_update:
            # Logic to follow if resource has dependencies
            if docker_resource.depends_on is not None:
                # 1. Reverse the order of dependencies
                docker_resource.depends_on.reverse()

                # 2. Remove the dependencies if they are already added to the final_docker_resources
                for dep in docker_resource.depends_on:
                    if dep in final_docker_resources:
                        logger.debug(f"-*- Removing {dep.name}, dependency of {docker_resource.name}")
                        final_docker_resources.remove(dep)

                # 3. Add the resource to be updated before its dependencies
                if docker_resource not in final_docker_resources:
                    logger.debug(f"-*- Adding {docker_resource.name}")
                    final_docker_resources.append(docker_resource)

                # 4. Add the dependencies back in reverse order
                for dep in docker_resource.depends_on:
                    if isinstance(dep, DockerResource):
                        if dep not in final_docker_resources:
                            logger.debug(f"-*- Adding {dep.name}, dependency of {docker_resource.name}")
                            final_docker_resources.append(dep)
            else:
                # Add the resource to be updated if it has no dependencies
                if docker_resource not in final_docker_resources:
                    logger.debug(f"-*- Adding {docker_resource.name}")
                    final_docker_resources.append(docker_resource)

        # Track the total number of DockerResources to update for validation
        num_resources_to_update: int = len(final_docker_resources)
        num_resources_updated: int = 0
        if num_resources_to_update == 0:
            print_info("No DockerResources to update")
            return

        if dry_run:
            print_heading("--**- Docker resources to update:")
            for resource in final_docker_resources:
                print_info(f"  -+-> {resource.get_resource_type()}: {resource.get_resource_name()}")
            print_info(f"\nNetwork: {self.network}")
            print_info(f"Total {num_resources_to_update} resources")
            return

        # Validate resources to be updated
        if not auto_confirm:
            print_heading("--**-- Confirm resources to update:")
            for resource in final_docker_resources:
                print_info(f"  -+-> {resource.get_resource_type()}: {resource.get_resource_name()}")
            print_info(f"\nNetwork: {self.network}")
            print_info(f"Total {num_resources_to_update} resources")
            confirm = confirm_yes_no("\nConfirm patch")
            if not confirm:
                print_info("-*-")
                print_info("-*- Skipping patch")
                print_info("-*-")
                exit(0)

        for resource in final_docker_resources:
            print_info(f"\n-==+==- {resource.get_resource_type()}: {resource.get_resource_name()}")
            if force is True:
                resource.force = True
            if isinstance(resource, DockerContainer):
                if resource.network is None and self.network is not None:
                    resource.network = self.network
            # logger.debug(resource)
            try:
                _resource_updated = resource.update(docker_client=self.docker_client)
                if _resource_updated:
                    num_resources_updated += 1
                else:
                    if workspace_settings is not None and not workspace_settings.continue_on_patch_failure:
                        return False
            except Exception as e:
                logger.error(f"Failed to update {resource.get_resource_type()}: {resource.get_resource_name()}")
                logger.error(e)
                logger.error("Please fix and try again...")

        print_info(f"\n# Resources updated: {num_resources_updated}/{num_resources_to_update}")
        if num_resources_to_update == num_resources_updated:
            return True

        logger.error(
            f"Resources updated: {num_resources_updated} do not match resources required: {num_resources_to_update}"  # noqa: E501
        )
        return False
