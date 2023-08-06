"""
Group Component for Smart Home - The Next Generation.

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

    class GroupComponent:
        pass


if typing.TYPE_CHECKING:
    from .group_component import GroupComponent


# pylint: disable=unused-variable
class Group(core.Entity):
    """Track a group of entity ids."""

    def __init__(
        self,
        owner: GroupComponent,
        name: str,
        order: int = None,
        icon: str = None,
        user_defined: bool = True,
        entity_ids: list[str] = None,
        mode=None,
    ):
        """Initialize a group.

        This Object has factory function for creation.
        """
        self._owner = owner
        self._shc = owner.controller
        self._name = name
        self._state = None
        self._icon = icon
        self._set_tracked(entity_ids)
        self._on_off = None
        self._assumed = None
        self._on_states = None
        self._user_defined = user_defined
        self._mode = any
        if mode:
            self._mode = all
        self._order = order
        self._assumed_state = False
        self._async_unsub_state_changed = None

    @staticmethod
    def create_group(
        owner: GroupComponent,
        name: str,
        entity_ids: list[str] = None,
        user_defined: bool = True,
        icon: str = None,
        object_id: str = None,
        mode=None,
        order: int = None,
    ):
        """Initialize a group."""
        return owner.controller.run_coroutine_threadsafe(
            Group.async_create_group(
                owner, name, entity_ids, user_defined, icon, object_id, mode, order
            ),
        ).result()

    @property
    def mode(self) -> bool:
        return self._mode == all

    @mode.setter
    def mode(self, value: bool) -> None:
        self._mode = all if value else any

    @property
    def user_defined(self) -> bool:
        return self._user_defined

    @property
    def entity_id(self) -> str:
        return super().entity_id

    @entity_id.setter
    def entity_id(self, value: str) -> None:
        if super()._entity_id is None:
            super()._entity_id = value

    @staticmethod
    async def async_create_group(
        owner: GroupComponent,
        name: str,
        entity_ids: list[str] = None,
        user_defined: bool = True,
        icon: str = None,
        object_id: str = None,
        mode=None,
        order: int = None,
    ):
        """Initialize a group.

        This method must be run in the event loop.
        """
        if order is None:
            order = owner.get_group_order()

        group = Group(
            owner,
            name,
            order=order,
            icon=icon,
            user_defined=user_defined,
            entity_ids=entity_ids,
            mode=mode,
        )

        group.entity_id = core.helpers.async_generate_entity_id(
            owner.domain + ".{}", object_id or name, shc=owner.controller
        )

        await owner.async_add_entities([group])

        return group

    @property
    def should_poll(self):
        """No need to poll because groups will update themselves."""
        return False

    @property
    def name(self):
        """Return the name of the group."""
        return self._name

    @name.setter
    def name(self, value):
        """Set Group name."""
        self._name = value

    @property
    def state(self):
        """Return the state of the group."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the group."""
        return self._icon

    @icon.setter
    def icon(self, value):
        """Set Icon for group."""
        self._icon = value

    @icon.setter
    def icon(self, value: str) -> None:
        self._icon = value

    @property
    def extra_state_attributes(self):
        """Return the state attributes for the group."""
        data = {core.Const.ATTR_ENTITY_ID: self.tracking, Const.ATTR_ORDER: self._order}
        if not self._user_defined:
            data[Const.ATTR_AUTO] = True

        return data

    @property
    def assumed_state(self):
        """Test if any member has an assumed state."""
        return self._assumed_state

    def update_tracked_entity_ids(self, entity_ids):
        """Update the member entity IDs."""
        self._owner.controller.run_coroutine_threadsafe(
            self.async_update_tracked_entity_ids(entity_ids)
        ).result()

    async def async_update_tracked_entity_ids(self, entity_ids):
        """Update the member entity IDs.

        This method must be run in the event loop.
        """
        self._async_stop()
        self._set_tracked(entity_ids)
        self._reset_tracked_state()
        self._async_start()

    def _set_tracked(self, entity_ids):
        """Tuple of entities to be tracked."""
        # tracking are the entities we want to track
        # trackable are the entities we actually watch

        if not entity_ids:
            self.tracking = ()
            self.trackable = ()
            return

        excluded_domains = self._owner.state_registry.exclude_domains

        tracking = []
        trackable = []
        for ent_id in entity_ids:
            ent_id_lower = ent_id.lower()
            domain = core.helpers.split_entity_id(ent_id_lower)[0]
            tracking.append(ent_id_lower)
            if domain not in excluded_domains:
                trackable.append(ent_id_lower)

        self.trackable = tuple(trackable)
        self.tracking = tuple(tracking)

    @core.callback
    def _async_start(self, *_):
        """Start tracking members and write state."""
        self._reset_tracked_state()
        self._async_start_tracking()
        self.async_write_state()

    @core.callback
    def _async_start_tracking(self):
        """Start tracking members.

        This method must be run in the event loop.
        """
        if self.trackable and self._async_unsub_state_changed is None:
            self._async_unsub_state_changed = (
                self._owner.controller.tracker.async_track_state_change_event(
                    self.trackable, self._async_state_changed_listener
                )
            )

        self._async_update_group_state()

    @core.callback
    def _async_stop(self):
        """Unregister the group from Home Assistant.

        This method must be run in the event loop.
        """
        if self._async_unsub_state_changed:
            self._async_unsub_state_changed()
            self._async_unsub_state_changed = None

    @core.callback
    def async_update_group_state(self):
        """Query all members and determine current group state."""
        self._state = None
        self._async_update_group_state()

    async def async_added_to_shc(self):
        """Handle addition to Home Assistant."""
        self.async_on_remove(self._shc.async_at_start(self._async_start))

    async def async_will_remove_from_shc(self):
        """Handle removal from Home Assistant."""
        self._async_stop()

    async def _async_state_changed_listener(self, event):
        """Respond to a member state changing.

        This method must be run in the event loop.
        """
        # removed
        if self._async_unsub_state_changed is None:
            return

        self.async_set_context(event.context)

        if (new_state := event.data.get("new_state")) is None:
            # The state was removed from the state machine
            self._reset_tracked_state()

        self._async_update_group_state(new_state)
        self.async_write_state()

    def _reset_tracked_state(self):
        """Reset tracked state."""
        self._on_off = {}
        self._assumed = {}
        self._on_states = set()

        for entity_id in self.trackable:
            if (state := self._shc.states.get(entity_id)) is not None:
                self._see_state(state)

    def _see_state(self, new_state):
        """Keep track of the the state."""
        entity_id = new_state.entity_id
        domain = new_state.domain
        state = new_state.state
        self._assumed[entity_id] = new_state.attributes.get(
            core.Const.ATTR_ASSUMED_STATE
        )
        registry = self._owner.state_registry

        if domain not in registry.on_states_by_domain:
            # Handle the group of a group case
            if state in registry.on_off_mapping:
                self._on_states.add(state)
            elif state in registry.off_on_mapping:
                self._on_states.add(registry.off_on_mapping[state])
            self._on_off[entity_id] = state in registry.on_off_mapping
        else:
            entity_on_state = registry.on_states_by_domain[domain]
            self._on_states.update(entity_on_state)
            self._on_off[entity_id] = state in entity_on_state

    @core.callback
    def _async_update_group_state(self, tr_state=None):
        """Update group state.

        Optionally you can provide the only state changed since last update
        allowing this method to take shortcuts.

        This method must be run in the event loop.
        """
        # To store current states of group entities. Might not be needed.
        if tr_state:
            self._see_state(tr_state)

        if not self._on_off:
            return

        if (
            tr_state is None
            or self._assumed_state
            and not tr_state.attributes.get(core.Const.ATTR_ASSUMED_STATE)
        ):
            self._assumed_state = self._mode(self._assumed.values())

        elif tr_state.attributes.get(core.Const.ATTR_ASSUMED_STATE):
            self._assumed_state = True

        num_on_states = len(self._on_states)
        # If all the entity domains we are tracking
        # have the same on state we use this state
        # and its hass.data[REG_KEY].on_off_mapping to off
        if num_on_states == 1:
            on_state = list(self._on_states)[0]
        # If we do not have an on state for any domains
        # we use None (which will be STATE_UNKNOWN)
        elif num_on_states == 0:
            self._state = None
            return
        # If the entity domains have more than one
        # on state, we use STATE_ON/STATE_OFF
        else:
            on_state = core.Const.STATE_ON
        group_is_on = self._mode(self._on_off.values())
        if group_is_on:
            self._state = on_state
        else:
            self._state = self._owner.state_registry.on_off_mapping[on_state]
