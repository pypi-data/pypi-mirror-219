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

import datetime as dt
import typing

from .action_condition_platform import ActionConditionPlatform
from .condition_checker_type import ConditionCheckerType
from .config_type import ConfigType
from .current_controller import _get_current_controller
from .script_condition import ScriptCondition
from .state import State
from .template import Template
from .template_vars_type import TemplateVarsType


# pylint: disable=unused-variable
class ConditionPlatform(ActionConditionPlatform):
    """Default Implementation for Components."""

    def async_numeric_state(
        self,
        entity: str | State,
        below: float | str = None,
        above: float | str = None,
        value_template: Template = None,
        variables: TemplateVarsType = None,
        attribute: str = None,
    ) -> bool:
        default_impl = ScriptCondition.get_action_condition_protocol(
            _get_current_controller()
        )
        return default_impl.async_numeric_state(
            entity, below, above, value_template, variables, attribute
        )

    def state_validate_config(self, config: ConfigType) -> ConfigType:
        """Validate state condition config."""
        default_impl: ScriptCondition = ScriptCondition.get_action_condition_protocol(
            _get_current_controller()
        )
        return default_impl.state_validate_config(config)

    def state_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Wrap action method with state based condition."""
        default_impl: ScriptCondition = ScriptCondition.get_action_condition_protocol(
            _get_current_controller()
        )
        return default_impl.state_from_config(config)

    # pylint: disable=unused-argument
    def zone(
        self,
        zone_ent: str | State,
        entity: str | State,
    ) -> bool:
        """Test if zone-condition matches.

        Async friendly.
        """
        default_impl: ScriptCondition = ScriptCondition.get_action_condition_protocol(
            _get_current_controller()
        )
        return default_impl.zone(zone_ent, entity)

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
        default_impl: ScriptCondition = ScriptCondition.get_action_condition_protocol(
            _get_current_controller()
        )
        return default_impl.state(entity, req_state, for_period, attribute)

    def numeric_state_validate_config(self, config: ConfigType) -> ConfigType:
        """Validate numeric_state condition config."""
        default_impl: ScriptCondition = ScriptCondition.get_action_condition_protocol(
            _get_current_controller()
        )
        return default_impl.numeric_state_validate_config(config)

    def async_numeric_state_from_config(
        self, config: ConfigType
    ) -> ConditionCheckerType:
        """Wrap action method with state based condition."""
        default_impl: ScriptCondition = ScriptCondition.get_action_condition_protocol(
            _get_current_controller()
        )
        return default_impl.async_numeric_state_from_config(config)
