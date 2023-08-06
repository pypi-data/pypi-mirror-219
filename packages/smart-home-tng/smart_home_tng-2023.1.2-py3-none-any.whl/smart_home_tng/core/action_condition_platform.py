"""
Core components of Smart Home - The Next Generation.

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

import abc
import datetime as dt
import typing

import voluptuous as vol

from .condition_checker_type import ConditionCheckerType
from .config_type import ConfigType
from .platform_implementation import PlatformImplementation
from .state import State
from .template import Template
from .template_vars_type import TemplateVarsType
from .trace import Trace


# pylint: disable=unused-variable
class ActionConditionPlatform(PlatformImplementation):
    """Define the format of device_condition modules.

    Each module must define either CONDITION_SCHEMA or async_validate_condition_config.
    """

    @property
    def condition_schema(self) -> typing.Callable[[ConfigType], ConfigType]:
        """
        Return the condition schema, or none if async_validate_condition
        should be called.
        """
        return None

    async def async_validate_condition_config(self, config: ConfigType) -> ConfigType:
        """Validate config."""
        schema = self.condition_schema
        if schema is not None:
            # pylint: disable=not-callable
            return schema(config)
        raise NotImplementedError()

    @abc.abstractmethod
    @Trace.condition_function
    async def async_condition_from_config(
        self, config: ConfigType
    ) -> ConditionCheckerType:
        """Evaluate state based on configuration."""

    # pylint: disable=unused-argument
    async def async_get_condition_capabilities(
        self, config: ConfigType
    ) -> dict[str, vol.Schema]:
        """List condition capabilities."""
        # default impl does nothing
        return None

    # pylint: disable=unused-argument
    async def async_get_conditions(self, device_id: str) -> list[dict[str, str]]:
        """List conditions."""
        return None

    def async_numeric_state(
        self,
        entity: str | State,
        below: float | str = None,
        above: float | str = None,
        value_template: Template = None,
        variables: TemplateVarsType = None,
        attribute: str = None,
    ) -> bool:
        """Test a numeric state condition."""
        return False

    def state_validate_config(self, config: ConfigType) -> ConfigType:
        """Validate state condition config."""
        return config

    # pylint: disable=unused-argument
    def state_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Wrap action method with state based condition."""
        return None

    # pylint: disable=unused-argument
    def zone(
        self,
        zone_ent: str | State,
        entity: str | State,
    ) -> bool:
        """Test if zone-condition matches.

        Async friendly.
        """
        return False

    # pylint: disable=unused-argument
    def state(
        self,
        entity: str | State,
        req_state: typing.Any,
        for_period: dt.timedelta = None,
        attribute: str = None,
    ) -> bool:
        """Test if state matches requirements.

        Async friendly.
        """
        return False

    def numeric_state_validate_config(self, config: ConfigType) -> ConfigType:
        """Validate numeric_state condition config."""
        return config

    def async_numeric_state_from_config(
        self, config: ConfigType
    ) -> ConditionCheckerType:
        """Wrap action method with state based condition."""
        return None
