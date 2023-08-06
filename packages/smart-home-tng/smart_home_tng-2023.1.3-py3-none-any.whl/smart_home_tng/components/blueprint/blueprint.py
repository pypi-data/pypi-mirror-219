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

import awesomeversion as asv
import voluptuous as vol
import yaml

from ... import core
from .const import Const
from .invalid_blueprint import InvalidBlueprint


# pylint: disable=unused-variable
class Blueprint(core.BlueprintBase):
    """Blueprint of a configuration structure."""

    def __init__(
        self,
        data: dict,
        *,
        path: str = None,
        expected_domain: str = None,
    ) -> None:
        """Initialize a blueprint."""
        try:
            data = self._data = Const.BLUEPRINT_SCHEMA(data)
        except vol.Invalid as err:
            raise InvalidBlueprint(expected_domain, path, data, err) from err

        # In future, we will treat this as "incorrect" and allow to recover from this
        data_domain = data[Const.CONF_BLUEPRINT][core.Const.CONF_DOMAIN]
        if expected_domain is not None and data_domain != expected_domain:
            raise InvalidBlueprint(
                expected_domain,
                path or self.name,
                data,
                f"Found incorrect blueprint type {data_domain}, expected {expected_domain}",
            )

        self._domain = data_domain

        missing = core.YamlLoader.extract_inputs(data) - set(
            data[Const.CONF_BLUEPRINT][Const.CONF_INPUT]
        )

        if missing:
            raise InvalidBlueprint(
                data_domain,
                path or self.name,
                data,
                f"Missing input definition for {', '.join(missing)}",
            )

    @property
    def name(self) -> str:
        """Return blueprint name."""
        return self._data[Const.CONF_BLUEPRINT][core.Const.CONF_NAME]

    @property
    def inputs(self) -> dict:
        """Return blueprint inputs."""
        return self._data[Const.CONF_BLUEPRINT][Const.CONF_INPUT]

    @property
    def metadata(self) -> dict:
        """Return blueprint metadata."""
        return self._data[Const.CONF_BLUEPRINT]

    def update_metadata(self, *, source_url: str = None) -> None:
        """Update metadata."""
        if source_url is not None:
            self._data[Const.CONF_BLUEPRINT][Const.CONF_SOURCE_URL] = source_url

    def yaml(self) -> str:
        """Dump blueprint as YAML."""
        return yaml.dump(self._data)

    @core.callback
    def validate(self) -> list[str]:
        """Test if the Home Assistant installation supports this blueprint.

        Return list of errors if not valid.
        """
        errors = []
        metadata = self.metadata
        min_version = metadata.get(Const.CONF_SMART_HOME_CONTROLLER, {}).get(
            Const.CONF_MIN_VERSION
        )

        if min_version is not None and asv.AwesomeVersion(
            core.Const.__version__
        ) < asv.AwesomeVersion(min_version):
            errors.append(
                f"Requires at least Smart Home - The Next Generation {min_version}"
            )

        return errors or None
