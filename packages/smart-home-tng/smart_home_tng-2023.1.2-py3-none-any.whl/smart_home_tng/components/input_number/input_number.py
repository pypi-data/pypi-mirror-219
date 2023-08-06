"""
Input Number Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core

_input_number: typing.TypeAlias = core.InputNumber


# pylint: disable=unused-variable
class InputNumber(core.RestoreEntity):
    """Representation of a slider."""

    _domain: str

    def __init__(self, config: dict) -> None:
        """Initialize an input number."""
        self._config = config
        self._editable = True
        self._current_value: float = config.get(_input_number.CONF_INITIAL)

    @property
    def editable(self) -> bool:
        return self._editable

    @classmethod
    def from_yaml(cls, config: dict):
        """Return entity instance initialized from yaml storage."""
        input_num = cls(config)
        input_num.entity_id = f"{InputNumber._domain}.{config[core.Const.CONF_ID]}"
        input_num.editable = False
        return input_num

    @property
    def should_poll(self):
        """If entity should be polled."""
        return False

    @property
    def _minimum(self) -> float:
        """Return minimum allowed value."""
        return self._config[_input_number.CONF_MIN]

    @property
    def _maximum(self) -> float:
        """Return maximum allowed value."""
        return self._config[_input_number.CONF_MAX]

    @property
    def name(self):
        """Return the name of the input slider."""
        return self._config.get(core.Const.CONF_NAME)

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return self._config.get(core.Const.CONF_ICON)

    @property
    def state(self):
        """Return the state of the component."""
        return self._current_value

    @property
    def _step(self) -> int:
        """Return entity's increment/decrement step."""
        return self._config[_input_number.CONF_STEP]

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._config.get(core.Const.CONF_UNIT_OF_MEASUREMENT)

    @property
    def unique_id(self) -> str:
        """Return unique id of the entity."""
        return self._config[core.Const.CONF_ID]

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            _input_number.ATTR_INITIAL: self._config.get(_input_number.CONF_INITIAL),
            core.Const.ATTR_EDITABLE: self.editable,
            _input_number.ATTR_MIN: self._minimum,
            _input_number.ATTR_MAX: self._maximum,
            _input_number.ATTR_STEP: self._step,
            core.Const.ATTR_MODE: self._config[core.Const.CONF_MODE],
        }

    async def async_added_to_shc(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_shc()
        if self._current_value is not None:
            return

        state = await self.async_get_last_state()
        value = state and float(state.state)

        # Check against None because value can be 0
        if value is not None and self._minimum <= value <= self._maximum:
            self._current_value = value
        else:
            self._current_value = self._minimum

    async def async_set_value(self, value):
        """Set new value."""
        num_value = float(value)

        if num_value < self._minimum or num_value > self._maximum:
            raise vol.Invalid(
                f"Invalid value for {self.entity_id}: {value} "
                + f"(range {self._minimum} - {self._maximum})"
            )

        self._current_value = num_value
        self.async_write_state()

    async def async_increment(self):
        """Increment value."""
        await self.async_set_value(min(self._current_value + self._step, self._maximum))

    async def async_decrement(self):
        """Decrement value."""
        await self.async_set_value(max(self._current_value - self._step, self._minimum))

    async def async_update_config(self, config: dict) -> None:
        """Handle when the config is updated."""
        self._config = config
        # just in case min/max values changed
        if self._current_value is None:
            return
        self._current_value = min(self._current_value, self._maximum)
        self._current_value = max(self._current_value, self._minimum)
        self.async_write_state()
