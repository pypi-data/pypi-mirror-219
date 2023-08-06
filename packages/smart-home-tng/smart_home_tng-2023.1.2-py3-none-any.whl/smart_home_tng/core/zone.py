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

import logging
import typing

from .callback import callback
from .callback_type import CallbackType
from .config_type import ConfigType
from .const import Const
from .event import Event
from .location_info import LocationInfo
from .script_condition import ScriptCondition
from .smart_home_controller_job import SmartHomeControllerJob
from .trigger_action_type import TriggerActionType
from .trigger_info import TriggerInfo

_LOGGER: typing.Final = logging.getLogger(__name__)

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_EVENT_ENTER: typing.Final = "zone.enter"
_EVENT_LEAVE: typing.Final = "zone.leave"
_DEFAULT_EVENT: typing.Final = _EVENT_ENTER

_EVENT_DESCRIPTION: typing.Final = {_EVENT_ENTER: "entering", _EVENT_LEAVE: "leaving"}


# pylint: disable=unused-variable, invalid-name
class Zone:
    """Zone namespace."""

    DEFAULT_EVENT: typing.Final = _DEFAULT_EVENT
    EVENT_DESCRIPTION: typing.Final = _EVENT_DESCRIPTION
    EVENT_ENTER: typing.Final = _EVENT_ENTER
    EVENT_LEAVE: typing.Final = _EVENT_LEAVE

    @staticmethod
    async def async_attach_trigger(
        shc: SmartHomeController,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
        platform_type="zone",
    ) -> CallbackType:
        """Listen for state changes based on configuration."""
        trigger_data = trigger_info["trigger_data"]
        entity_id: list[str] = config[Const.CONF_ENTITY_ID]
        zone_entity_id = config.get(Const.CONF_ZONE)
        event = config.get(Const.CONF_EVENT)
        job = SmartHomeControllerJob(action)

        @callback
        def zone_automation_listener(zone_event: Event):
            """Listen for state changes and calls action."""
            entity = zone_event.data.get("entity_id")
            from_s = zone_event.data.get("old_state")
            to_s = zone_event.data.get("new_state")

            if (
                from_s
                and not LocationInfo.has_location(from_s)
                or not LocationInfo.has_location(to_s)
            ):
                return

            if not (zone_state := shc.states.get(zone_entity_id)):
                _LOGGER.warning(
                    f"Automation '{trigger_info['name']}' is referencing non-existing "
                    + f"zone '{zone_entity_id}' in a zone trigger",
                )
                return

            cond = ScriptCondition.get_action_condition_protocol(shc)
            from_match = cond.zone(zone_state, from_s) if from_s else False
            to_match = cond.zone(zone_state, to_s) if to_s else False

            if (
                event == _EVENT_ENTER
                and not from_match
                and to_match
                or event == _EVENT_LEAVE
                and from_match
                and not to_match
            ):
                description = (
                    f"{entity} {_EVENT_DESCRIPTION[event]} "
                    + f"{zone_state.attributes[Const.ATTR_FRIENDLY_NAME]}"
                )
                shc.async_run_shc_job(
                    job,
                    {
                        "trigger": {
                            **trigger_data,
                            "platform": platform_type,
                            "entity_id": entity,
                            "from_state": from_s,
                            "to_state": to_s,
                            "zone": zone_state,
                            "event": event,
                            "description": description,
                        }
                    },
                    to_s.context,
                )

        return shc.tracker.async_track_state_change_event(
            entity_id, zone_automation_listener
        )
