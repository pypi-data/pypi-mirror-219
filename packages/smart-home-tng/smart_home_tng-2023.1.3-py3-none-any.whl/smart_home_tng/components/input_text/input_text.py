"""
Input Text Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class InputText(core.RestoreEntity):
    """Represent a text box."""

    _domain: str

    def __init__(self, config: dict) -> None:
        """Initialize a text input."""
        self._config = config
        self._editable = True
        self._current_value = config.get(Const.CONF_INITIAL)

    @property
    def editable(self) -> bool:
        return self._editable

    @classmethod
    def from_yaml(cls, config: dict):
        """Return entity instance initialized from yaml storage."""
        input_text = cls(config)
        input_text.entity_id = f"{InputText._domain}.{config[core.Const.CONF_ID]}"
        input_text.editable = False
        return input_text

    @property
    def should_poll(self):
        """If entity should be polled."""
        return False

    @property
    def name(self):
        """Return the name of the text input entity."""
        return self._config.get(core.Const.CONF_NAME)

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return self._config.get(core.Const.CONF_ICON)

    @property
    def _maximum(self) -> int:
        """Return max len of the text."""
        return self._config[Const.CONF_MAX]

    @property
    def _minimum(self) -> int:
        """Return min len of the text."""
        return self._config[Const.CONF_MIN]

    @property
    def state(self):
        """Return the state of the component."""
        return self._current_value

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._config.get(core.Const.CONF_UNIT_OF_MEASUREMENT)

    @property
    def unique_id(self) -> str:
        """Return unique id for the entity."""
        return self._config[core.Const.CONF_ID]

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            core.Const.ATTR_EDITABLE: self.editable,
            Const.ATTR_MIN: self._minimum,
            Const.ATTR_MAX: self._maximum,
            Const.ATTR_PATTERN: self._config.get(Const.CONF_PATTERN),
            core.Const.ATTR_MODE: self._config[core.Const.CONF_MODE],
        }

    async def async_added_to_shc(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_shc()
        if self._current_value is not None:
            return

        state = await self.async_get_last_state()
        value = state and state.state

        # Check against None because value can be 0
        if value is not None and self._minimum <= len(value) <= self._maximum:
            self._current_value = value

    async def async_set_value(self, value):
        """Select new value."""
        if len(value) < self._minimum or len(value) > self._maximum:
            _LOGGER.warning(
                f"Invalid value: {value} (length range {self._minimum} - {self._maximum})",
            )
            return
        self._current_value = value
        self.async_write_state()

    async def async_update_config(self, config: dict) -> None:
        """Handle when the config is updated."""
        self._config = config
        self.async_write_state()
