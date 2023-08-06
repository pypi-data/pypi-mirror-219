"""
Switch As X Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class BaseEntity(core.Entity):
    """Represents a Switch as a X."""

    _attr_should_poll = False

    def __init__(
        self,
        name: str,
        switch_entity_id: str,
        unique_id: str,
        device_id: str = None,
    ) -> None:
        """Initialize Light Switch."""
        self._device_id = device_id
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._switch_entity_id = switch_entity_id

    # pylint: disable=attribute-defined-outside-init
    @core.callback
    def async_state_changed_listener(self, _event: core.Event = None) -> None:
        """Handle child updates."""
        if (
            state := self._shc.states.get(self._switch_entity_id)
        ) is None or state.state == core.Const.STATE_UNAVAILABLE:
            self._attr_available = False
            return

        self._attr_available = True

    async def async_added_to_shc(self) -> None:
        """Register callbacks."""

        @core.callback
        def _async_state_changed_listener(event: core.Event = None) -> None:
            """Handle child updates."""
            self.async_state_changed_listener(event)
            self.async_write_state()

        self.async_on_remove(
            self._shc.tracker.async_track_state_change_event(
                [self._switch_entity_id], _async_state_changed_listener
            )
        )

        # Call once on adding
        _async_state_changed_listener()

        # Add this entity to the wrapped switch's device
        registry = self._shc.entity_registry
        if registry.async_get(self.entity_id) is not None:
            registry.async_update_entity(self.entity_id, device_id=self._device_id)
