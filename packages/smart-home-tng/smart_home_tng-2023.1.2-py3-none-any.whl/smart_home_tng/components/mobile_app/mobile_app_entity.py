"""
Mobile App Component for Smart Home - The Next Generation.

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

if not typing.TYPE_CHECKING:

    class MobileAppComponent:
        pass


if typing.TYPE_CHECKING:
    from .mobile_app_component import MobileAppComponent


# pylint: disable=unused-variable
class MobileAppEntity(core.RestoreEntity):
    """Representation of an mobile app entity."""

    _attr_should_poll = False

    def __init__(
        self,
        owner: MobileAppComponent,
        config: dict,
        entry: core.ConfigEntry,
    ) -> None:
        """Initialize the entity."""
        self._config = config
        self._entry = entry
        self._registration = entry.data
        self._attr_unique_id = config[core.Const.CONF_UNIQUE_ID]
        self._name = self._config[core.Const.CONF_NAME]
        self._owner = owner

    async def async_added_to_shc(self):
        """Register callbacks."""
        signal_sensor_update = self._owner.domain + ".sensor.update"
        self.async_on_remove(
            self._owner.controller.dispatcher.async_connect(
                signal_sensor_update, self._handle_update
            )
        )

        if (state := await self.async_get_last_state()) is None:
            return

        self.async_restore_last_state(state)

    @core.callback
    def async_restore_last_state(self, last_state):
        """Restore previous state."""
        self._config[Const.ATTR_SENSOR_STATE] = last_state.state
        self._config[Const.ATTR_SENSOR_ATTRIBUTES] = {
            **last_state.attributes,
            **self._config[Const.ATTR_SENSOR_ATTRIBUTES],
        }
        if core.Const.ATTR_ICON in last_state.attributes:
            self._config[Const.ATTR_SENSOR_ICON] = last_state.attributes[
                core.Const.ATTR_ICON
            ]

    @property
    def name(self):
        """Return the name of the mobile app sensor."""
        return self._name

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if entity should be enabled by default."""
        return not self._config.get(Const.ATTR_SENSOR_DISABLED)

    @property
    def device_class(self):
        """Return the device class."""
        return str(self._config.get(Const.ATTR_SENSOR_DEVICE_CLASS))

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        return self._config[Const.ATTR_SENSOR_ATTRIBUTES]

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._config[Const.ATTR_SENSOR_ICON]

    @property
    def entity_category(self):
        """Return the entity category, if any."""
        return self._config.get(Const.ATTR_SENSOR_ENTITY_CATEGORY)

    @property
    def device_info(self):
        """Return device registry information for this entity."""
        # pylint: disable=protected-access
        return self._owner._device_info(self._registration)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._config.get(Const.ATTR_SENSOR_STATE) != core.Const.STATE_UNAVAILABLE

    @core.callback
    def _handle_update(self, incoming_id, data):
        """Handle async event updates."""
        if incoming_id != self._attr_unique_id:
            return

        self._config = {**self._config, **data}
        self.async_write_state()
