"""
Person Tracking Component for Smart Home - The Next Generation.

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

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


def _get_latest(prev: core.State, curr: core.State) -> core.State:
    """Get latest state."""
    if prev is None or curr.last_updated > prev.last_updated:
        return curr
    return prev


# pylint: disable=unused-variable
class Person(core.RestoreEntity):
    """Represent a tracked person."""

    def __init__(self, config):
        """Set up person."""
        self._config = config
        self._editable = True
        self._latitude = None
        self._longitude = None
        self._gps_accuracy = None
        self._source = None
        self._state = None
        self._unsub_track_device = None

    @property
    def editable(self) -> bool:
        return self._editable

    @classmethod
    def from_yaml(cls, config):
        """Return entity instance initialized from yaml storage."""
        person = cls(config)
        person._editable = False
        return person

    @property
    def name(self):
        """Return the name of the entity."""
        return self._config[core.Const.CONF_NAME]

    @property
    def entity_picture(self) -> str:
        """Return entity picture."""
        return self._config.get(Const.CONF_PICTURE)

    @property
    def should_poll(self):
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return False

    @property
    def state(self):
        """Return the state of the person."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the person."""
        data = {
            core.Const.ATTR_EDITABLE: self.editable,
            core.Const.ATTR_ID: self.unique_id,
        }
        if self._latitude is not None:
            data[core.Const.ATTR_LATITUDE] = self._latitude
        if self._longitude is not None:
            data[core.Const.ATTR_LONGITUDE] = self._longitude
        if self._gps_accuracy is not None:
            data[core.Const.ATTR_GPS_ACCURACY] = self._gps_accuracy
        if self._source is not None:
            data[Const.ATTR_SOURCE] = self._source
        if (user_id := self._config.get(Const.CONF_USER_ID)) is not None:
            data[Const.ATTR_USER_ID] = user_id
        return data

    @property
    def unique_id(self):
        """Return a unique ID for the person."""
        return self._config[core.Const.CONF_ID]

    async def async_added_to_shc(self):
        """Register device trackers."""
        await super().async_added_to_shc()
        if state := await self.async_get_last_state():
            self._parse_source_state(state)

        if self._shc.is_running:
            # Update person now if hass is already running.
            await self.async_update_config(self._config)
        else:
            # Wait for hass start to not have race between person
            # and device trackers finishing setup.
            self._shc.bus.async_listen_once(
                core.Const.EVENT_SHC_START, self._person_start_shc
            )

    async def _person_start_shc(self, _now):
        await self.async_update_config(self._config)

    async def async_update_config(self, config):
        """Handle when the config is updated."""
        self._config = config

        if self._unsub_track_device is not None:
            self._unsub_track_device()
            self._unsub_track_device = None

        if trackers := self._config[Const.CONF_DEVICE_TRACKERS]:
            _LOGGER.debug(f"Subscribe to device trackers for {self.entity_id}")

            self._unsub_track_device = self._shc.tracker.async_track_state_change_event(
                trackers, self._async_handle_tracker_update
            )

        self._update_state()

    @core.callback
    def _async_handle_tracker_update(self, _event):
        """Handle the device tracker state changes."""
        self._update_state()

    @core.callback
    def _update_state(self):
        """Update the state."""
        latest_non_gps_home = latest_not_home = latest_gps = latest = None
        for entity_id in self._config[Const.CONF_DEVICE_TRACKERS]:
            state = self._shc.states.get(entity_id)

            if not state or state.state in Const.IGNORE_STATES:
                continue

            if (
                state.attributes.get(core.Const.ATTR_SOURCE_TYPE)
                == core.TrackerSourceType.GPS
            ):
                latest_gps = _get_latest(latest_gps, state)
            elif state.state == core.Const.STATE_HOME:
                latest_non_gps_home = _get_latest(latest_non_gps_home, state)
            elif state.state == core.Const.STATE_NOT_HOME:
                latest_not_home = _get_latest(latest_not_home, state)

        if latest_non_gps_home:
            latest = latest_non_gps_home
        elif latest_gps:
            latest = latest_gps
        else:
            latest = latest_not_home

        if latest:
            self._parse_source_state(latest)
        else:
            self._state = None
            self._source = None
            self._latitude = None
            self._longitude = None
            self._gps_accuracy = None

        self.async_write_state()

    @core.callback
    def _parse_source_state(self, state):
        """Parse source state and set person attributes.

        This is a device tracker state or the restored person state.
        """
        self._state = state.state
        self._source = state.entity_id
        self._latitude = state.attributes.get(core.Const.ATTR_LATITUDE)
        self._longitude = state.attributes.get(core.Const.ATTR_LONGITUDE)
        self._gps_accuracy = state.attributes.get(core.Const.ATTR_GPS_ACCURACY)
