"""
Automation Integration for Smart Home - The Next Generation.

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

import logging
import typing


# pylint: disable=unused-variable
class Const:
    """Constants for the automation integration."""

    CONF_ACTION: typing.Final = "action"
    CONF_TRIGGER: typing.Final = "trigger"
    CONF_TRIGGER_VARIABLES: typing.Final = "trigger_variables"

    CONF_HIDE_ENTITY: typing.Final = "hide_entity"

    CONF_CONDITION_TYPE: typing.Final = "condition_type"
    CONF_INITIAL_STATE: typing.Final = "initial_state"
    CONF_BLUEPRINT: typing.Final = "blueprint"
    CONF_INPUT: typing.Final = "input"
    CONF_TRACE: typing.Final = "trace"

    DEFAULT_INITIAL_STATE: typing.Final = True

    LOGGER: typing.Final = logging.getLogger(__package__)

    CONF_SKIP_CONDITION: typing.Final = "skip_condition"
    CONF_STOP_ACTIONS: typing.Final = "stop_actions"
    DEFAULT_STOP_ACTIONS: typing.Final = True

    ATTR_LAST_TRIGGERED: typing.Final = "last_triggered"
    ATTR_SOURCE: typing.Final = "source"
    ATTR_VARIABLES: typing.Final = "variables"
    SERVICE_TRIGGER: typing.Final = "trigger"
