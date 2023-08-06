"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import logging
import typing

import alexapy

from ... import core
from .alexa_client import AlexaClient
from .alexa_media import AlexaMedia
from .helpers import _catch_login_errors

_switch: typing.TypeAlias = core.Switch

if not typing.TYPE_CHECKING:

    class AlexaAccountInfo:
        pass


if typing.TYPE_CHECKING:
    from .alexa_account_info import AlexaAccountInfo

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaMediaSwitch(core.Switch.Entity, AlexaMedia):
    """Representation of a Alexa Media switch."""

    def __init__(
        self,
        owner: AlexaAccountInfo,
        client: AlexaClient,
        switch_property: str,
        switch_function: str,
        name="Alexa",
    ):
        """Initialize the Alexa Switch device."""
        # Class info
        # pylint: disable=protected-access
        self._client = client
        self._name = name
        self._switch_property = switch_property
        self._switch_function = switch_function
        self._info = owner
        self._listener = None
        super().__init__(owner._owner, client, client._login)

    async def async_added_to_shc(self):
        """Store register state change callback."""
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        # Register event handler on bus
        self._listener = self._shc.dispatcher.async_connect(
            f"{self._owner.domain}_{alexapy.hide_email(self.email)}"[0:32],
            self._handle_event,
        )

    async def async_will_remove_from_shc(self):
        """Prepare to remove entity."""
        # Register event handler on bus
        self._listener()

    def _handle_event(self, event):
        """Handle events.

        This will update PUSH_MEDIA_QUEUE_CHANGE events to see if the switch
        should be updated.
        """
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        if "queue_state" in event:
            queue_state = event["queue_state"]
            if queue_state["dopplerId"]["deviceSerialNumber"] == self._client.unique_id:
                self.async_write_state()

    @_catch_login_errors
    async def _set_switch(self, state, **kwargs):
        # pylint: disable=unused-argument
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        success = await getattr(self._alexa_api, self._switch_function)(state)
        # if function returns success, make immediate state change
        if success:
            setattr(self._client, self._switch_property, state)
            _LOGGER.debug(
                f"Setting {self._name} to {state}",
            )
            self.async_write_state()
        elif self.should_poll:
            # if we need to poll, refresh media_client
            _LOGGER.debug(
                f"Requesting update of {self._client} due to {self._name} switch to {state}",
            )
            await self._client.async_update()

    @property
    def is_on(self):
        """Return true if on."""
        return self.available and getattr(self._client, self._switch_property)

    async def async_turn_on(self, **kwargs):
        """Turn on switch."""
        await self._set_switch(True, **kwargs)

    async def async_turn_off(self, **kwargs):
        """Turn off switch."""
        await self._set_switch(False, **kwargs)

    @property
    def available(self):
        """Return the availability of the switch."""
        return (
            self._client.available
            and getattr(self._client, self._switch_property) is not None
        )

    @property
    def assumed_state(self):
        """Return whether the state is an assumed_state."""
        return self._client.assumed_state

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self._client.unique_id + "_" + self._name

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{self._client.name} {self._name} switch"

    @property
    def device_class(self):
        """Return the device_class of the switch."""
        return _switch.DeviceClass.SWITCH

    @property
    def hidden(self):
        """Return whether the switch should be hidden from the UI."""
        return not self.available

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @_catch_login_errors
    async def async_update(self):
        """Update state."""
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        try:
            self.async_write_state()
        except core.NoEntitySpecifiedError:
            pass  # we ignore this due to a harmless startup race condition

    @property
    def device_info(self):
        """Return device_info for device registry."""
        return {
            "identifiers": {(self._owner.domain, self._client.unique_id)},
        }

    @property
    def icon(self):
        """Return the icon of the switch."""
        return self._icon()

    def _icon(self, on=None, off=None):
        # pylint: disable=invalid-name
        return on if self.is_on else off
