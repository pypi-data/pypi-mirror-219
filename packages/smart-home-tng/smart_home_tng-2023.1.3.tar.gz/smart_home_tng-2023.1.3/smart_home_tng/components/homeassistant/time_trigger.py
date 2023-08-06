"""
Core pieces for Smart Home - The Next Generation.

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
import functools
import typing

import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation

_TIME_TRIGGER_SCHEMA: typing.Final = vol.Any(
    _cv.time,
    vol.All(str, _cv.entity_domain(["input_datetime", "sensor"])),
    msg="Expected HH:MM, HH:MM:SS or Entity ID with domain 'input_datetime' or 'sensor'",
)

_TRIGGER_SCHEMA: typing.Final = _cv.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_PLATFORM): "time",
        vol.Required(core.Const.CONF_AT): vol.All(
            _cv.ensure_list, [_TIME_TRIGGER_SCHEMA]
        ),
    }
)


# pylint: disable=unused-variable
class TimeTrigger(core.TriggerPlatform):
    """Offer time listening automation rules."""

    def __init__(self, shc: core.SmartHomeController) -> None:
        super().__init__()
        self._shc = shc

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        return _TRIGGER_SCHEMA(config)

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for state changes based on configuration."""
        trigger_data = trigger_info["trigger_data"]
        entities: dict[str, core.CallbackType] = {}
        removes = []
        job = core.SmartHomeControllerJob(action)
        tracker = self._shc.tracker

        @core.callback
        def time_automation_listener(description, now, *, entity_id=None):
            """Listen for time changes and calls action."""
            self._shc.async_run_shc_job(
                job,
                {
                    "trigger": {
                        **trigger_data,
                        "platform": "time",
                        "now": now,
                        "description": description,
                        "entity_id": entity_id,
                    }
                },
            )

        @core.callback
        def update_entity_trigger_event(event):
            """update_entity_trigger from the event."""
            return update_entity_trigger(
                event.data["entity_id"], event.data["new_state"]
            )

        @core.callback
        def update_entity_trigger(entity_id, new_state=None):
            """Update the entity trigger for the entity_id."""
            # If a listener was already set up for entity, remove it.
            if remove := entities.pop(entity_id, None):
                remove()
                remove = None

            if not new_state:
                return

            # Check state of entity. If valid, set up a listener.
            if new_state.domain == "input_datetime":
                if has_date := new_state.attributes["has_date"]:
                    year = new_state.attributes["year"]
                    month = new_state.attributes["month"]
                    day = new_state.attributes["day"]
                if has_time := new_state.attributes["has_time"]:
                    hour = new_state.attributes["hour"]
                    minute = new_state.attributes["minute"]
                    second = new_state.attributes["second"]
                else:
                    # If no time then use midnight.
                    hour = minute = second = 0

                if has_date:
                    # If input_datetime has date, then track point in time.
                    trigger_dt = dt.datetime(
                        year,
                        month,
                        day,
                        hour,
                        minute,
                        second,
                        tzinfo=core.helpers.get_default_time_zone(),
                    )
                    # Only set up listener if time is now or in the future.
                    if trigger_dt >= core.helpers.now():
                        remove = tracker.async_track_point_in_time(
                            functools.partial(
                                time_automation_listener,
                                f"time set in {entity_id}",
                                entity_id=entity_id,
                            ),
                            trigger_dt,
                        )
                elif has_time:
                    # Else if it has time, then track time change.
                    remove = tracker.async_track_time_change(
                        functools.partial(
                            time_automation_listener,
                            f"time set in {entity_id}",
                            entity_id=entity_id,
                        ),
                        hour=hour,
                        minute=minute,
                        second=second,
                    )
            elif (
                new_state.domain == "sensor"
                and new_state.attributes.get(core.Const.ATTR_DEVICE_CLASS)
                == core.Sensor.DeviceClass.TIMESTAMP
                and new_state.state
                not in (core.Const.STATE_UNAVAILABLE, core.Const.STATE_UNKNOWN)
            ):
                trigger_dt = core.helpers.parse_datetime(new_state.state)

                if trigger_dt is not None and trigger_dt > core.helpers.utcnow():
                    remove = tracker.async_track_point_in_time(
                        functools.partial(
                            time_automation_listener,
                            f"time set in {entity_id}",
                            entity_id=entity_id,
                        ),
                        trigger_dt,
                    )

            # Was a listener set up?
            if remove:
                entities[entity_id] = remove

        to_track = []

        for at_time in config[core.Const.CONF_AT]:
            if isinstance(at_time, str):
                # entity
                to_track.append(at_time)
                update_entity_trigger(at_time, new_state=self._shc.states.get(at_time))
            else:
                # datetime.time
                removes.append(
                    tracker.async_track_time_change(
                        functools.partial(time_automation_listener, "time"),
                        hour=at_time.hour,
                        minute=at_time.minute,
                        second=at_time.second,
                    )
                )

        # Track state changes of any entities.
        removes.append(
            tracker.async_track_state_change_event(
                to_track, update_entity_trigger_event
            )
        )

        @core.callback
        def remove_track_time_changes():
            """Remove tracked time changes."""
            for remove in entities.values():
                remove()
            for remove in removes:
                remove()

        return remove_track_time_changes
