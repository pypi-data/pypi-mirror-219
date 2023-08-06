"""
Blueprint Integration for Smart Home - The Next Generation.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022-2023, Andreas Nixdorf

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program.  If not, see
http://www.gnu.org/licenses/.
"""

import asyncio
import logging
import pathlib
import shutil

import voluptuous as vol
import voluptuous.humanize as vh

from ... import core
from .blueprint import Blueprint
from .blueprint_exception import BlueprintException
from .blueprint_inputs import BlueprintInputs
from .const import Const
from .failed_to_load import FailedToLoad
from .file_already_exists import FileAlreadyExists
from .invalid_blueprint_inputs import InvalidBlueprintInputs


# pylint: disable=unused-variable
class DomainBlueprints(core.DomainBlueprintsBase):
    """Blueprints for a specific domain."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        domain: str,
        logger: logging.Logger,
    ) -> None:
        """Initialize a domain blueprints instance."""
        self._shc = shc
        self._domain = domain
        self._logger = logger
        self._blueprints = {}
        self._load_lock = asyncio.Lock()

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def blueprint_folder(self) -> pathlib.Path:
        """Return the blueprint folder."""
        return pathlib.Path(self._shc.config.path(Const.BLUEPRINT_FOLDER, self.domain))

    @core.callback
    def reset_cache(self) -> None:
        """Reset the blueprint cache."""
        self._blueprints = {}

    def _load_blueprint(self, blueprint_path) -> Blueprint:
        """Load a blueprint."""
        try:
            blueprint_data = core.YamlLoader.load_yaml(
                self.blueprint_folder / blueprint_path
            )
        except FileNotFoundError as err:
            raise FailedToLoad(
                self.domain,
                blueprint_path,
                FileNotFoundError(f"Unable to find {blueprint_path}"),
            ) from err
        except core.SmartHomeControllerError as err:
            raise FailedToLoad(self.domain, blueprint_path, err) from err

        return Blueprint(
            blueprint_data, expected_domain=self.domain, path=blueprint_path
        )

    def _load_blueprints(self) -> dict[str, Blueprint | BlueprintException]:
        """Load all the blueprints."""
        blueprint_folder = pathlib.Path(
            self._shc.config.path(Const.BLUEPRINT_FOLDER, self.domain)
        )
        results = {}

        for blueprint_path in blueprint_folder.glob("**/*.yaml"):
            blueprint_path = str(blueprint_path.relative_to(blueprint_folder))
            if self._blueprints.get(blueprint_path) is None:
                try:
                    self._blueprints[blueprint_path] = self._load_blueprint(
                        blueprint_path
                    )
                except BlueprintException as err:
                    self._blueprints[blueprint_path] = None
                    results[blueprint_path] = err
                    continue

            results[blueprint_path] = self._blueprints[blueprint_path]

        return results

    async def async_get_blueprints(
        self,
    ) -> dict[str, Blueprint | BlueprintException]:
        """Get all the blueprints."""
        async with self._load_lock:
            return await self._shc.async_add_executor_job(self._load_blueprints)

    async def async_get_blueprint(self, blueprint_path: str) -> Blueprint:
        """Get a blueprint."""

        def load_from_cache():
            """Load blueprint from cache."""
            if (blueprint := self._blueprints[blueprint_path]) is None:
                raise FailedToLoad(
                    self.domain,
                    blueprint_path,
                    FileNotFoundError(f"Unable to find {blueprint_path}"),
                )
            return blueprint

        if blueprint_path in self._blueprints:
            return load_from_cache()

        async with self._load_lock:
            # Check it again
            if blueprint_path in self._blueprints:
                return load_from_cache()

            try:
                blueprint = await self._shc.async_add_executor_job(
                    self._load_blueprint, blueprint_path
                )
            except Exception:
                self._blueprints[blueprint_path] = None
                raise

            self._blueprints[blueprint_path] = blueprint
            return blueprint

    async def async_inputs_from_config(
        self, config_with_blueprint: dict
    ) -> BlueprintInputs:
        """Process a blueprint config."""
        try:
            config_with_blueprint = Const.BLUEPRINT_INSTANCE_FIELDS(
                config_with_blueprint
            )
        except vol.Invalid as err:
            raise InvalidBlueprintInputs(
                self.domain, vh.humanize_error(config_with_blueprint, err)
            ) from err

        bp_conf = config_with_blueprint[Const.CONF_USE_BLUEPRINT]
        blueprint = await self.async_get_blueprint(bp_conf[core.Const.CONF_PATH])
        inputs = BlueprintInputs(blueprint, config_with_blueprint)
        inputs.validate()
        return inputs

    async def async_remove_blueprint(self, blueprint_path: str) -> None:
        """Remove a blueprint file."""
        path = self.blueprint_folder / blueprint_path
        await self._shc.async_add_executor_job(path.unlink)
        self._blueprints[blueprint_path] = None

    def _create_file(self, blueprint: Blueprint, blueprint_path: str) -> None:
        """Create blueprint file."""

        path = pathlib.Path(
            self._shc.config.path(Const.BLUEPRINT_FOLDER, self.domain, blueprint_path)
        )
        if path.exists():
            raise FileAlreadyExists(self.domain, blueprint_path)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(blueprint.yaml(), encoding="utf-8")

    async def async_add_blueprint(
        self, blueprint: Blueprint, blueprint_path: str
    ) -> None:
        """Add a blueprint."""
        if not blueprint_path.endswith(".yaml"):
            blueprint_path = f"{blueprint_path}.yaml"

        await self._shc.async_add_executor_job(
            self._create_file, blueprint, blueprint_path
        )

        self._blueprints[blueprint_path] = blueprint

    async def async_populate(self) -> None:
        """Create folder if it doesn't exist and populate with examples."""
        integration = await self._shc.setup.async_get_integration(self.domain)

        def populate():
            if self.blueprint_folder.exists():
                return

            shutil.copytree(
                integration.file_path / Const.BLUEPRINT_FOLDER,
                self.blueprint_folder / Const.SHC_FOLDER,
            )

        await self._shc.async_add_executor_job(populate)
