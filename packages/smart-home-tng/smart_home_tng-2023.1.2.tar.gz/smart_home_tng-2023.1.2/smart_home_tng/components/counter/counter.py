"""
Counter Integration for Smart Home - The Next Generation.

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

from ... import core
from .const import Const


# pylint: disable=unused-variable
class Counter(core.RestoreEntity):
    """Representation of a counter."""

    def __init__(self, config: dict, domain: str, editable: bool = True) -> None:
        """Initialize a counter."""
        self._state: int = config[Const.CONF_INITIAL]
        self._editable: bool = editable
        self._entity_id = Const.ENTITY_ID_FORMAT.format(
            domain, config[core.Const.CONF_ID]
        )
        self._name: str = None
        self._icon: str = None
        self._step: int = 1
        self._min: int = None
        self._max: int = None
        self._unique_id: str = None
        self._restore: bool = False
        self._update_from_dict(config)
        self._initial = self._state

    def _update_from_dict(self, values: core.ConfigType, is_config: bool = True):
        """Set values from config dict or service call."""
        if is_config:
            self._name = values[core.Const.CONF_NAME]
            self._icon = values.get(core.Const.CONF_ICON)
            self._unique_id = values[core.Const.CONF_ID]
            self._restore: bool = values[Const.CONF_RESTORE]
        key = Const.CONF_STEP if is_config else Const.ATTR_STEP
        if is_config or key in values:
            self._step = values[key]
        key = Const.CONF_INITIAL if is_config else Const.ATTR_INITIAL
        if is_config or key in values:
            self._initial = values[key]
        key = core.Const.CONF_MINIMUM if is_config else Const.ATTR_MINIMUM
        if is_config or key in values:
            self._min = values[key]
        key = core.Const.CONF_MAXIMUM if is_config else Const.ATTR_MAXIMUM
        if is_config or key in values:
            self._max = values[key]

    @classmethod
    def from_yaml(cls, domain: str, config: dict):
        """Create counter instance from yaml config."""
        counter = cls(config, domain, False)
        return counter

    @property
    def should_poll(self) -> bool:
        """If entity should be polled."""
        return False

    @property
    def name(self) -> str:
        """Return name of the counter."""
        return self._name

    @property
    def icon(self) -> str:
        """Return the icon to be used for this entity."""
        return self._icon

    @property
    def state(self) -> int:
        """Return the current value of the counter."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        ret = {
            core.Const.ATTR_EDITABLE: self._editable,
            Const.ATTR_INITIAL: self._initial,
            Const.ATTR_STEP: self._step,
        }
        if self._min is not None:
            ret[core.Const.CONF_MINIMUM] = self._min
        if self._max is not None:
            ret[core.Const.CONF_MAXIMUM] = self._max
        return ret

    @property
    def unique_id(self) -> str:
        """Return unique id of the entity."""
        return self._unique_id

    def compute_next_state(self, state) -> int:
        """Keep the state within the range of min/max values."""
        if self._min is not None:
            state = max(self._min, state)
        if self._max is not None:
            state = min(self._max, state)

        return state

    async def async_added_to_shc(self) -> None:
        """Call when entity about to be added to Smart Home - The Next Generation."""
        await super().async_added_to_shc()
        # __init__ will set self._state to self._initial, only override
        # if needed.
        if self._restore and (state := await self.async_get_last_state()) is not None:
            self._state = self.compute_next_state(int(state.state))
            self._initial = state.attributes.get(Const.ATTR_INITIAL)
            self._max = state.attributes.get(Const.ATTR_MAXIMUM)
            self._min = state.attributes.get(Const.ATTR_MINIMUM)
            self._step = state.attributes.get(Const.ATTR_STEP)

    @core.callback
    def async_decrement(self) -> None:
        """Decrement the counter."""
        self._state = self.compute_next_state(self._state - self._step)
        self.async_write_state()

    @core.callback
    def async_increment(self) -> None:
        """Increment a counter."""
        self._state = self.compute_next_state(self._state + self._step)
        self.async_write_state()

    @core.callback
    def async_reset(self) -> None:
        """Reset a counter."""
        self._state = self.compute_next_state(self._initial)
        self.async_write_state()

    @core.callback
    def async_configure(self, **kwargs) -> None:
        """Change the counter's settings with a service."""
        new_state = kwargs.pop(Const.VALUE, self._state)
        self._update_from_dict(kwargs, False)
        self._state = self.compute_next_state(new_state)
        self.async_write_state()

    async def async_update_config(self, config: dict) -> None:
        """Change the counter's settings WS CRUD."""
        self._update_from_dict(config)
        self._state = self.compute_next_state(self._state)
        self.async_write_state()
