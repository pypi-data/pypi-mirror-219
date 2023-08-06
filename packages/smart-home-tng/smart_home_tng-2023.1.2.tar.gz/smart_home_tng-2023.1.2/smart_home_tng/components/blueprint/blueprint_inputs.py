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

import typing

from ... import core
from .const import Const
from .missing_input import MissingInput


if not typing.TYPE_CHECKING:

    class Blueprint:
        ...


if typing.TYPE_CHECKING:
    from .blueprint import Blueprint


# pylint: disable=unused-variable
class BlueprintInputs(core.BlueprintInputsBase):
    """Inputs for a blueprint."""

    def __init__(
        self, blueprint: Blueprint, config_with_inputs: dict[str, typing.Any]
    ) -> None:
        """Instantiate a blueprint inputs object."""
        self._blueprint = blueprint
        self._config_with_inputs = config_with_inputs

    @property
    def blueprint(self) -> core.BlueprintBase:
        return self._blueprint

    @property
    def config_with_inputs(self) -> core.ConfigType:
        return self._config_with_inputs

    @property
    def inputs(self):
        """Return the inputs."""
        return self._config_with_inputs[Const.CONF_USE_BLUEPRINT][Const.CONF_INPUT]

    @property
    def inputs_with_default(self):
        """Return the inputs and fallback to defaults."""
        no_input = set(self._blueprint.inputs) - set(self.inputs)

        inputs_with_default = dict(self.inputs)

        for inp in no_input:
            blueprint_input = self._blueprint.inputs[inp]
            if (
                isinstance(blueprint_input, dict)
                and core.Const.CONF_DEFAULT in blueprint_input
            ):
                inputs_with_default[inp] = blueprint_input[core.Const.CONF_DEFAULT]

        return inputs_with_default

    def validate(self) -> None:
        """Validate the inputs."""
        missing = set(self._blueprint.inputs) - set(self.inputs_with_default)

        if missing:
            raise MissingInput(self.blueprint.domain, self.blueprint.name, missing)

        # In future we can see if entities are correct domain, areas exist etc
        # using the new selector helper.

    @core.callback
    def async_substitute(self) -> dict:
        """Get the blueprint value with the inputs substituted."""
        processed = core.YamlLoader.substitute(
            self._blueprint.data, self.inputs_with_default
        )
        combined = {**processed, **self.config_with_inputs}
        # From config_with_inputs
        combined.pop(Const.CONF_USE_BLUEPRINT)
        # From blueprint
        combined.pop(Const.CONF_BLUEPRINT)
        return combined
