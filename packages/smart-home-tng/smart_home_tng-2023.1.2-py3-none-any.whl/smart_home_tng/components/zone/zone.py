"""
Zone Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class Zone(core.Entity):
    """Representation of a Zone."""

    def __init__(self, config: dict) -> None:
        """Initialize the zone."""
        self._config = config
        if core.Const.CONF_ENTITY_ID in config:
            self._entity_id = config[core.Const.CONF_ENTITY_ID]
        self._editable = True
        self._attrs: dict = None
        self._remove_listener: typing.Callable[[], None] = None
        self._persons_in_zone: set[str] = set()
        self._generate_attrs()

    @property
    def editable(self) -> bool:
        return self._editable

    @classmethod
    def from_yaml(cls, config: dict):
        """Return entity instance initialized from yaml storage."""
        zone = cls(config)
        zone.editable = False
        zone._generate_attrs()
        return zone

    @property
    def state(self) -> int:
        """Return the state property really does nothing for a zone."""
        return len(self._persons_in_zone)

    @property
    def name(self) -> str:
        """Return name."""
        return typing.cast(str, self._config[core.Const.CONF_NAME])

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return self._config.get(core.Const.CONF_ID)

    @property
    def icon(self) -> str:
        """Return the icon if any."""
        return self._config.get(core.Const.CONF_ICON)

    @property
    def should_poll(self) -> bool:
        """Zone does not poll."""
        return False

    async def async_update_config(self, config: dict) -> None:
        """Handle when the config is updated."""
        if self._config == config:
            return
        self._config = config
        self._generate_attrs()
        self.async_write_state()

    @core.callback
    def _person_state_change_listener(self, evt: core.Event) -> None:
        person_entity_id = evt.data[core.Const.ATTR_ENTITY_ID]
        cur_count = len(self._persons_in_zone)
        if self._state_is_in_zone(evt.data.get("new_state")):
            self._persons_in_zone.add(person_entity_id)
        elif person_entity_id in self._persons_in_zone:
            self._persons_in_zone.remove(person_entity_id)

        if len(self._persons_in_zone) != cur_count:
            self._generate_attrs()
            self.async_write_state()

    async def async_added_to_shc(self) -> None:
        """Run when entity about to be added to Smart Home TNG."""
        await super().async_added_to_shc()
        person_domain = core.Const.PERSON_COMPONENT_NAME
        persons = self._shc.states.async_entity_ids(person_domain)
        for person in persons:
            if self._state_is_in_zone(self._shc.states.get(person)):
                self._persons_in_zone.add(person)
        self._generate_attrs()

        self.async_on_remove(
            self._shc.tracker.async_track_state_change_filtered(
                core.TrackStates(False, set(), {person_domain}),
                self._person_state_change_listener,
            ).async_remove
        )

    @core.callback
    def _generate_attrs(self) -> None:
        """Generate new attrs based on config."""
        self._attr_extra_state_attributes = {
            core.Const.ATTR_LATITUDE: self._config[core.Const.CONF_LATITUDE],
            core.Const.ATTR_LONGITUDE: self._config[core.Const.CONF_LONGITUDE],
            Const.ATTR_RADIUS: self._config[core.Const.CONF_RADIUS],
            Const.ATTR_PASSIVE: self._config[Const.CONF_PASSIVE],
            core.Const.ATTR_PERSONS: sorted(self._persons_in_zone),
            core.Const.ATTR_EDITABLE: self.editable,
        }

    @core.callback
    def _state_is_in_zone(self, state: core.State) -> bool:
        """Return if given state is in zone."""
        return (
            state is not None
            and state.state
            not in (
                core.Const.STATE_NOT_HOME,
                core.Const.STATE_UNKNOWN,
                core.Const.STATE_UNAVAILABLE,
            )
            and (
                state.state.casefold() == self.name.casefold()
                or (
                    state.state == core.Const.STATE_HOME
                    and self.entity_id == Const.ENTITY_ID_HOME
                )
            )
        )
