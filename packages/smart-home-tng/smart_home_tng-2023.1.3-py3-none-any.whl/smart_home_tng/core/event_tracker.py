"""
Core components of Smart Home - The Next Generation.

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

import asyncio
import collections.abc
import copy
import datetime
import logging
import time
import typing

from . import helpers
from .callback import callback
from .callback_type import CallbackType
from .const import Const
from .event import Event
from .keyed_rate_limit import KeyedRateLimit
from .render_info import RenderInfo
from .smart_home_controller_job import SmartHomeControllerJob
from .state import State
from .template import Template
from .template_error import TemplateError
from .template_vars_type import TemplateVarsType
from .track_states import TrackStates
from .track_template import TrackTemplate
from .track_template_result import TrackTemplateResult
from .track_template_result_listener import TrackTemplateResultListener
from .sun_listener import SunListener


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_TRACK_STATE_CHANGE_CALLBACKS: typing.Final = "track_state_change_callbacks"
_TRACK_STATE_CHANGE_LISTENER: typing.Final = "track_state_change_listener"

_TRACK_STATE_ADDED_DOMAIN_CALLBACKS: typing.Final = "track_state_added_domain_callbacks"
_TRACK_STATE_ADDED_DOMAIN_LISTENER: typing.Final = "track_state_added_domain_listener"

_TRACK_STATE_REMOVED_DOMAIN_CALLBACKS: typing.Final = (
    "track_state_removed_domain_callbacks"
)
_TRACK_STATE_REMOVED_DOMAIN_LISTENER: typing.Final = (
    "track_state_removed_domain_listener"
)

_TRACK_ENTITY_REGISTRY_UPDATED_CALLBACKS: typing.Final = (
    "track_entity_registry_updated_callbacks"
)
_TRACK_ENTITY_REGISTRY_UPDATED_LISTENER: typing.Final = (
    "track_entity_registry_updated_listener"
)

_ALL_LISTENER = "all"
_DOMAINS_LISTENER = "domains"
_ENTITIES_LISTENER = "entities"

_LOGGER: typing.Final = logging.getLogger(__name__)


class _TrackTemplateResultInfo:
    """Handle removal / refresh of tracker."""

    def __init__(
        self,
        shc: SmartHomeController,
        track_templates: collections.abc.Sequence[TrackTemplate],
        action: collections.abc.Callable[[Event, list[TrackTemplateResult]], None],
        has_super_template: bool = False,
    ) -> None:
        """Handle removal / refresh of tracker init."""
        self._shc = shc
        self._job = SmartHomeControllerJob(action)

        for track_template_ in track_templates:
            track_template_.template.controller = shc
        self._track_templates = track_templates
        self._has_super_template = has_super_template

        self._last_result: dict[Template, bool | str | TemplateError] = {}

        self._rate_limit = KeyedRateLimit(shc)
        self._info: dict[Template, RenderInfo] = {}
        self._track_state_changes: _TrackStateChangeFiltered = None
        self._time_listeners: dict[Template, collections.abc.Callable[[], None]] = {}

    def async_setup(self, raise_on_template_error: bool, strict: bool = False) -> None:
        """Activation of template tracking."""
        block_render = False
        super_template = self._track_templates[0] if self._has_super_template else None

        # Render the super template first
        if super_template is not None:
            template = super_template.template
            variables = super_template.variables
            self._info[template] = info = template.async_render_to_info(
                variables, strict=strict
            )

            # If the super template did not render to True, don't update other templates
            try:
                super_result: str | TemplateError = info.result()
            except TemplateError as ex:
                super_result = ex
            if (
                super_result is not None
                and self._super_template_as_boolean(super_result) is not True
            ):
                block_render = True

        # Then update the remaining templates unless blocked by the super template
        for track_template_ in self._track_templates:
            if block_render or track_template_ == super_template:
                continue
            template = track_template_.template
            variables = track_template_.variables
            self._info[template] = info = template.async_render_to_info(
                variables, strict=strict
            )

            if info.exception:
                if raise_on_template_error:
                    raise info.exception
                _LOGGER.error(
                    f"Error while processing template: {track_template_.template}",
                    exc_info=info.exception,
                )

        self._track_state_changes = self._shc.tracker.async_track_state_change_filtered(
            _render_infos_to_track_states(self._info.values()), self._refresh
        )
        self._update_time_listeners()
        _LOGGER.debug(
            f"Template group {self._track_templates} listens for {self.listeners}, "
            + f"first render blocker by super template: {block_render}"
        )

    @property
    def listeners(self) -> dict[str, bool | set[str]]:
        """State changes that will cause a re-render."""
        assert self._track_state_changes
        return {
            **self._track_state_changes.listeners,
            "time": bool(self._time_listeners),
        }

    @callback
    def _setup_time_listener(self, template: Template, has_time: bool) -> None:
        if not has_time:
            if template in self._time_listeners:
                # now() or utcnow() has left the scope of the template
                self._time_listeners.pop(template)()
            return

        if template in self._time_listeners:
            return

        track_templates = [
            track_template_
            for track_template_ in self._track_templates
            if track_template_.template == template
        ]

        @callback
        def _refresh_from_time(_now: datetime.datetime) -> None:
            self._refresh(None, track_templates=track_templates)

        self._time_listeners[template] = self._shc.async_track_utc_time_change(
            _refresh_from_time, second=0
        )

    @callback
    def _update_time_listeners(self) -> None:
        for template, info in self._info.items():
            self._setup_time_listener(template, info.has_time)

    @callback
    def async_remove(self) -> None:
        """Cancel the listener."""
        assert self._track_state_changes
        self._track_state_changes.async_remove()
        self._rate_limit.async_remove()
        for template in list(self._time_listeners):
            self._time_listeners.pop(template)()

    @callback
    def async_refresh(self) -> None:
        """Force recalculate the template."""
        self._refresh(None)

    def _render_template_if_ready(
        self,
        track_template_: TrackTemplate,
        now: datetime.datetime,
        event: Event,
    ) -> bool | TrackTemplateResult:
        """Re-render the template if conditions match.

        Returns False if the template was not re-rendered.

        Returns True if the template re-rendered and did not
        change.

        Returns TrackTemplateResult if the template re-render
        generates a new result.
        """
        template = track_template_.template

        if event:
            info = self._info[template]

            if not _event_triggers_rerender(event, info):
                return False

            had_timer = self._rate_limit.async_has_timer(template)

            if self._rate_limit.async_schedule_action(
                template,
                _rate_limit_for_event(event, info, track_template_),
                now,
                self._refresh,
                event,
                (track_template_,),
                True,
            ):
                return not had_timer

            _LOGGER.debug(
                f"Template update {template.template_code} triggered by event: {event}"
            )

        self._rate_limit.async_triggered(template, now)
        self._info[template] = info = template.async_render_to_info(
            track_template_.variables
        )

        try:
            result: str | TemplateError = info.result()
        except TemplateError as ex:
            result = ex

        last_result = self._last_result.get(template)

        # Check to see if the result has changed or is new
        if result == last_result and template in self._last_result:
            return True

        if isinstance(result, TemplateError) and isinstance(last_result, TemplateError):
            return True

        return TrackTemplateResult(template, last_result, result)

    @staticmethod
    def _super_template_as_boolean(result: bool | str | TemplateError) -> bool:
        """Return True if the result is truthy or a TemplateError."""
        if isinstance(result, TemplateError):
            return True

        return Template.result_as_boolean(result)

    @callback
    def _refresh(
        self,
        event: Event,
        track_templates: collections.abc.Iterable[TrackTemplate] = None,
        replayed: bool = False,
    ) -> None:
        """Refresh the template.

        The event is the state_changed event that caused the refresh
        to be considered.

        track_templates is an optional list of TrackTemplate objects
        to refresh.  If not provided, all tracked templates will be
        considered.

        replayed is True if the event is being replayed because the
        rate limit was hit.
        """
        updates: list[TrackTemplateResult] = []
        info_changed = False
        now = event.time_fired if not replayed and event else helpers.utcnow()

        def _apply_update(
            update: bool | TrackTemplateResult, template: Template
        ) -> bool:
            """Handle updates of a tracked template."""
            if not update:
                return False

            self._setup_time_listener(template, self._info[template].has_time)

            if isinstance(update, TrackTemplateResult):
                updates.append(update)

            return True

        block_updates = False
        super_template = self._track_templates[0] if self._has_super_template else None

        track_templates = track_templates or self._track_templates

        # Update the super template first
        if super_template is not None:
            update = self._render_template_if_ready(super_template, now, event)
            info_changed |= _apply_update(update, super_template.template)

            if isinstance(update, TrackTemplateResult):
                super_result = update.result
            else:
                super_result = self._last_result.get(super_template.template)

            # If the super template did not render to True, don't update other templates
            if (
                super_result is not None
                and self._super_template_as_boolean(super_result) is not True
            ):
                block_updates = True

            if (
                isinstance(update, TrackTemplateResult)
                and self._super_template_as_boolean(update.last_result) is not True
                and self._super_template_as_boolean(update.result) is True
            ):
                # Super template changed from not True to True, force re-render
                # of all templates in the group
                event = None
                track_templates = self._track_templates

        # Then update the remaining templates unless blocked by the super template
        if not block_updates:
            for track_template_ in track_templates:
                if track_template_ == super_template:
                    continue

                update = self._render_template_if_ready(track_template_, now, event)
                info_changed |= _apply_update(update, track_template_.template)

        if info_changed:
            assert self._track_state_changes
            self._track_state_changes.async_update_listeners(
                _render_infos_to_track_states(
                    [
                        _suppress_domain_all_in_render_info(info)
                        if self._rate_limit.async_has_timer(template)
                        else info
                        for template, info in self._info.items()
                    ]
                )
            )
            _LOGGER.debug(
                f"Template group {self._track_templates} listens for {self.listeners}, "
                + f"re-render blocker by super template:{block_updates}",
            )

        if not updates:
            return

        for track_result in updates:
            self._last_result[track_result.template] = track_result.result

        self._shc.async_run_shc_job(self._job, event, updates)


class _TrackStateChangeFiltered:
    """Handle removal / refresh of tracker."""

    def __init__(
        self,
        shc: SmartHomeController,
        track_states: TrackStates,
        action: collections.abc.Callable[[Event], typing.Any],
    ) -> None:
        """Handle removal / refresh of tracker init."""
        self._shc = shc
        self._action = action
        self._action_as_hassjob = SmartHomeControllerJob(action)
        self._listeners: dict[str, collections.abc.Callable[[], None]] = {}
        self._last_track_states: TrackStates = track_states

    @callback
    def async_setup(self) -> None:
        """Create listeners to track states."""
        track_states = self._last_track_states

        if (
            not track_states.all_states
            and not track_states.domains
            and not track_states.entities
        ):
            return

        if track_states.all_states:
            self._setup_all_listener()
            return

        self._setup_domains_listener(track_states.domains)
        self._setup_entities_listener(track_states.domains, track_states.entities)

    @property
    def listeners(self) -> dict[str, bool | set[str]]:
        """State changes that will cause a re-render."""
        track_states = self._last_track_states
        return {
            _ALL_LISTENER: track_states.all_states,
            _ENTITIES_LISTENER: track_states.entities,
            _DOMAINS_LISTENER: track_states.domains,
        }

    @callback
    def async_update_listeners(self, new_track_states: TrackStates) -> None:
        """Update the listeners based on the new TrackStates."""
        last_track_states = self._last_track_states
        self._last_track_states = new_track_states

        had_all_listener = last_track_states.all_states

        if new_track_states.all_states:
            if had_all_listener:
                return
            self._cancel_listener(_DOMAINS_LISTENER)
            self._cancel_listener(_ENTITIES_LISTENER)
            self._setup_all_listener()
            return

        if had_all_listener:
            self._cancel_listener(_ALL_LISTENER)

        domains_changed = new_track_states.domains != last_track_states.domains

        if had_all_listener or domains_changed:
            domains_changed = True
            self._cancel_listener(_DOMAINS_LISTENER)
            self._setup_domains_listener(new_track_states.domains)

        if (
            had_all_listener
            or domains_changed
            or new_track_states.entities != last_track_states.entities
        ):
            self._cancel_listener(_ENTITIES_LISTENER)
            self._setup_entities_listener(
                new_track_states.domains, new_track_states.entities
            )

    @callback
    def async_remove(self) -> None:
        """Cancel the listeners."""
        for key in list(self._listeners):
            self._listeners.pop(key)()

    @callback
    def _cancel_listener(self, listener_name: str) -> None:
        if listener_name not in self._listeners:
            return

        self._listeners.pop(listener_name)()

    @callback
    def _setup_entities_listener(self, domains: set[str], entities: set[str]) -> None:
        if domains:
            entities = entities.copy()
            entities.update(self._shc.states.async_entity_ids(domains))

        # Entities has changed to none
        if not entities:
            return

        self._listeners[_ENTITIES_LISTENER] = _async_track_state_change_event(
            self._shc, entities, self._action
        )

    @callback
    def _state_added(self, event: Event) -> None:
        self._cancel_listener(_ENTITIES_LISTENER)
        self._setup_entities_listener(
            self._last_track_states.domains, self._last_track_states.entities
        )
        self._shc.async_run_shc_job(self._action_as_hassjob, event)

    @callback
    def _setup_domains_listener(self, domains: set[str]) -> None:
        if not domains:
            return

        self._listeners[_DOMAINS_LISTENER] = _async_track_state_added_domain(
            self._shc, domains, self._state_added
        )

    @callback
    def _setup_all_listener(self) -> None:
        self._listeners[_ALL_LISTENER] = self._shc.bus.async_listen(
            Const.EVENT_STATE_CHANGED, self._action
        )


# pylint: disable=unused-variable
class EventTracker:
    """Helpers for listening to events."""

    def __init__(self, shc: SmartHomeController):
        self._shc = shc

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    @staticmethod
    def process_state_match(
        parameter: str | collections.abc.Iterable[str], invert: bool = False
    ) -> collections.abc.Callable[[str], bool]:
        """Convert parameter to function that matches input against parameter."""
        return _process_state_match(parameter, invert)

    @callback
    def async_track_state_change(
        self,
        entity_ids: str | collections.abc.Iterable[str],
        action: collections.abc.Callable[
            [str, State, State], collections.abc.Awaitable[None]
        ],
        from_state: str | collections.abc.Iterable[str] = None,
        to_state: str | collections.abc.Iterable[str] = None,
    ) -> CallbackType:
        """Track specific state changes.

        entity_ids, from_state and to_state can be string or list.
        Use list to match multiple.

        Returns a function that can be called to remove the listener.

        If entity_ids are not MATCH_ALL along with from_state and to_state
        being None, async_track_state_change_event should be used instead
        as it is slightly faster.

        Must be run within the event loop.
        """
        if from_state is not None:
            match_from_state = _process_state_match(from_state)
        if to_state is not None:
            match_to_state = _process_state_match(to_state)

        # Ensure it is a lowercase list with entity ids we want to match on
        if entity_ids == Const.MATCH_ALL:
            pass
        elif isinstance(entity_ids, str):
            entity_ids = (entity_ids.lower(),)
        else:
            entity_ids = tuple(entity_id.lower() for entity_id in entity_ids)

        job = SmartHomeControllerJob(action)

        @callback
        def state_change_filter(event: Event) -> bool:
            """Handle specific state changes."""
            if from_state is not None:
                if (old_state := event.data.get("old_state")) is not None:
                    old_state = old_state.state

                if not match_from_state(old_state):
                    return False

            if to_state is not None:
                if (new_state := event.data.get("new_state")) is not None:
                    new_state = new_state.state

                if not match_to_state(new_state):
                    return False

            return True

        @callback
        def state_change_dispatcher(event: Event) -> None:
            """Handle specific state changes."""
            self._shc.async_run_shc_job(
                job,
                event.data.get("entity_id"),
                event.data.get("old_state"),
                event.data.get("new_state"),
            )

        @callback
        def state_change_listener(event: Event) -> None:
            """Handle specific state changes."""
            if not state_change_filter(event):
                return

            state_change_dispatcher(event)

        if entity_ids != Const.MATCH_ALL:
            # If we have a list of entity ids we use
            # async_track_state_change_event to route
            # by entity_id to avoid iterating though state change
            # events and creating a jobs where the most
            # common outcome is to return right away because
            # the entity_id does not match since usually
            # only one or two listeners want that specific
            # entity_id.
            return self.async_track_state_change_event(
                entity_ids, state_change_listener
            )

        return self._shc.bus.async_listen(
            Const.EVENT_STATE_CHANGED,
            state_change_dispatcher,
            event_filter=state_change_filter,
        )

    def track_state_change(
        self,
        entity_ids: str | collections.abc.Iterable[str],
        action: collections.abc.Callable[
            [str, State, State], collections.abc.Awaitable[None]
        ],
        from_state: str | collections.abc.Iterable[str] = None,
        to_state: str | collections.abc.Iterable[str] = None,
    ) -> CallbackType:
        """Track specific state changes.

        entity_ids, from_state and to_state can be string or list.
        Use list to match multiple.

        Returns a function that can be called to remove the listener.

        If entity_ids are not MATCH_ALL along with from_state and to_state
        being None, async_track_state_change_event should be used instead
        as it is slightly faster.
        """
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_state_change, entity_ids, action, from_state, to_state
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    def async_track_state_change_event(
        self,
        entity_ids: str | collections.abc.Iterable[str],
        action: collections.abc.Callable[[Event], typing.Any],
    ) -> CallbackType:
        """Track specific state change events indexed by entity_id.

        Unlike async_track_state_change, async_track_state_change_event
        passes the full event to the callback.

        In order to avoid having to iterate a long list
        of EVENT_STATE_CHANGED and fire and create a job
        for each one, we keep a dict of entity ids that
        care about the state change events so we can
        do a fast dict lookup to route events.
        """
        if not (entity_ids := _async_string_to_lower_list(entity_ids)):
            return _remove_empty_listener
        return _async_track_state_change_event(self._shc, entity_ids, action)

    def async_track_entity_registry_updated_event(
        self,
        entity_ids: str | collections.abc.Iterable[str],
        action: collections.abc.Callable[[Event], typing.Any],
    ) -> CallbackType:
        """Track specific entity registry updated events indexed by entity_id.

        Similar to async_track_state_change_event.
        """
        if not (entity_ids := _async_string_to_lower_list(entity_ids)):
            return _remove_empty_listener

        entity_callbacks = self._shc.data.setdefault(
            _TRACK_ENTITY_REGISTRY_UPDATED_CALLBACKS, {}
        )

        if _TRACK_ENTITY_REGISTRY_UPDATED_LISTENER not in self._shc.data:

            @callback
            def _async_entity_registry_updated_filter(event: Event) -> bool:
                """Filter entity registry updates by entity_id."""
                entity_id = event.data.get("old_entity_id", event.data["entity_id"])
                return entity_id in entity_callbacks

            @callback
            def _async_entity_registry_updated_dispatcher(event: Event) -> None:
                """Dispatch entity registry updates by entity_id."""
                entity_id = event.data.get("old_entity_id", event.data["entity_id"])

                if entity_id not in entity_callbacks:
                    return

                for job in entity_callbacks[entity_id][:]:
                    try:
                        self._shc.async_run_shc_job(job, event)
                    except Exception:  # pylint: disable=broad-except
                        _LOGGER.exception(
                            f"Error while processing entity registry update for {entity_id}"
                        )

            self._shc.data[
                _TRACK_ENTITY_REGISTRY_UPDATED_LISTENER
            ] = self._shc.bus.async_listen(
                Const.EVENT_ENTITY_REGISTRY_UPDATED,
                _async_entity_registry_updated_dispatcher,
                event_filter=_async_entity_registry_updated_filter,
            )

        job = SmartHomeControllerJob(action)

        for entity_id in entity_ids:
            entity_callbacks.setdefault(entity_id, []).append(job)

        @callback
        def remove_listener() -> None:
            """Remove state change listener."""
            _async_remove_indexed_listeners(
                self._shc,
                _TRACK_ENTITY_REGISTRY_UPDATED_CALLBACKS,
                _TRACK_ENTITY_REGISTRY_UPDATED_LISTENER,
                entity_ids,
                job,
            )

        return remove_listener

    def async_track_state_added_domain(
        self,
        domains: str | collections.abc.Iterable[str],
        action: collections.abc.Callable[[Event], typing.Any],
    ) -> CallbackType:
        """Track state change events when an entity is added to domains."""
        if not (domains := _async_string_to_lower_list(domains)):
            return _remove_empty_listener
        return self._async_track_state_added_domain(domains, action)

    def _async_track_state_added_domain(
        self,
        domains: str | collections.abc.Iterable[str],
        action: collections.abc.Callable[[Event], typing.Any],
    ) -> CallbackType:
        """async_track_state_added_domain without lowercasing."""
        domain_callbacks = self._shc.data.setdefault(
            _TRACK_STATE_ADDED_DOMAIN_CALLBACKS, {}
        )

        if _TRACK_STATE_ADDED_DOMAIN_LISTENER not in self._shc.data:

            @callback
            def _async_state_change_filter(event: Event) -> bool:
                """Filter state changes by entity_id."""
                return event.data.get("old_state") is None

            @callback
            def _async_state_change_dispatcher(event: Event) -> None:
                """Dispatch state changes by entity_id."""
                if event.data.get("old_state") is not None:
                    return

                _async_dispatch_domain_event(self._shc, event, domain_callbacks)

            self._shc.data[
                _TRACK_STATE_ADDED_DOMAIN_LISTENER
            ] = self._shc.bus.async_listen(
                Const.EVENT_STATE_CHANGED,
                _async_state_change_dispatcher,
                event_filter=_async_state_change_filter,
            )

        job = SmartHomeControllerJob(action)

        for domain in domains:
            domain_callbacks.setdefault(domain, []).append(job)

        @callback
        def remove_listener() -> None:
            """Remove state change listener."""
            _async_remove_indexed_listeners(
                self._shc,
                _TRACK_STATE_ADDED_DOMAIN_CALLBACKS,
                _TRACK_STATE_ADDED_DOMAIN_LISTENER,
                domains,
                job,
            )

        return remove_listener

    def async_track_state_removed_domain(
        self,
        domains: str | collections.abc.Iterable[str],
        action: collections.abc.Callable[[Event], typing.Any],
    ) -> CallbackType:
        """Track state change events when an entity is removed from domains."""
        if not (domains := _async_string_to_lower_list(domains)):
            return _remove_empty_listener

        domain_callbacks = self._shc.data.setdefault(
            _TRACK_STATE_REMOVED_DOMAIN_CALLBACKS, {}
        )

        if _TRACK_STATE_REMOVED_DOMAIN_LISTENER not in self._shc.data:

            @callback
            def _async_state_change_filter(event: Event) -> bool:
                """Filter state changes by entity_id."""
                return event.data.get("new_state") is None

            @callback
            def _async_state_change_dispatcher(event: Event) -> None:
                """Dispatch state changes by entity_id."""
                if event.data.get("new_state") is not None:
                    return

                _async_dispatch_domain_event(self._shc, event, domain_callbacks)

            self._shc.data[
                _TRACK_STATE_REMOVED_DOMAIN_LISTENER
            ] = self._shc.bus.async_listen(
                Const.EVENT_STATE_CHANGED,
                _async_state_change_dispatcher,
                event_filter=_async_state_change_filter,
            )

        job = SmartHomeControllerJob(action)

        for domain in domains:
            domain_callbacks.setdefault(domain, []).append(job)

        @callback
        def remove_listener() -> None:
            """Remove state change listener."""
            _async_remove_indexed_listeners(
                self._shc,
                _TRACK_STATE_REMOVED_DOMAIN_CALLBACKS,
                _TRACK_STATE_REMOVED_DOMAIN_LISTENER,
                domains,
                job,
            )

        return remove_listener

    @callback
    def async_track_state_change_filtered(
        self,
        track_states: TrackStates,
        action: collections.abc.Callable[[Event], typing.Any],
    ) -> _TrackStateChangeFiltered:
        """Track state changes with a TrackStates filter that can be updated.

        Parameters
        ----------
        hass
            Home assistant object.
        track_states
            A TrackStates data class.
        action
            Callable to call with results.

        Returns
        -------
        Object used to update the listeners (async_update_listeners) with a new TrackStates or
        cancel the tracking (async_remove).

        """
        tracker = _TrackStateChangeFiltered(self._shc, track_states, action)
        tracker.async_setup()
        return tracker

    @callback
    def async_track_template(
        self,
        template: Template,
        action: collections.abc.Callable[
            [str, State, State], collections.abc.Awaitable[None]
        ],
        variables: TemplateVarsType = None,
    ) -> CallbackType:
        """Add a listener that fires when a a template evaluates to 'true'.

        Listen for the result of the template becoming true, or a true-like
        string result, such as 'On', 'Open', or 'Yes'. If the template results
        in an error state when the value changes, this will be logged and not
        passed through.

        If the initial check of the template is invalid and results in an
        exception, the listener will still be registered but will only
        fire if the template result becomes true without an exception.

        Action arguments
        ----------------
        entity_id
            ID of the entity that triggered the state change.
        old_state
            The old state of the entity that changed.
        new_state
            New state of the entity that changed.

        Parameters
        ----------
        template
            The template to calculate.
        action
            Callable to call with results. See above for arguments.
        variables
            Variables to pass to the template.

        Returns
        -------
        Callable to unregister the listener.

        """
        job = SmartHomeControllerJob(action)

        @callback
        def _template_changed_listener(
            event: Event, updates: list[TrackTemplateResult]
        ) -> None:
            """Check if condition is correct and run action."""
            track_result = updates.pop()

            template = track_result.template
            last_result = track_result.last_result
            result = track_result.result

            if isinstance(result, TemplateError):
                _LOGGER.error(
                    f"Error while processing template: {template.template}",
                    exc_info=result,
                )
                return

            if (
                not isinstance(last_result, TemplateError)
                and Template.result_as_boolean(last_result)
                or not Template.result_as_boolean(result)
            ):
                return

            self._shc.async_run_shc_job(
                job,
                event and event.data.get("entity_id"),
                event and event.data.get("old_state"),
                event and event.data.get("new_state"),
            )

        info = self.async_track_template_result(
            [TrackTemplate(template, variables)], _template_changed_listener
        )

        return info.async_remove

    def track_template(
        self,
        template: Template,
        action: collections.abc.Callable[
            [str, State, State], collections.abc.Awaitable[None]
        ],
        variables: TemplateVarsType = None,
    ) -> CallbackType:
        """Add a listener that fires when a a template evaluates to 'true'.

        Listen for the result of the template becoming true, or a true-like
        string result, such as 'On', 'Open', or 'Yes'. If the template results
        in an error state when the value changes, this will be logged and not
        passed through.

        If the initial check of the template is invalid and results in an
        exception, the listener will still be registered but will only
        fire if the template result becomes true without an exception.

        Action arguments
        ----------------
        entity_id
            ID of the entity that triggered the state change.
        old_state
            The old state of the entity that changed.
        new_state
            New state of the entity that changed.

        Parameters
        ----------
        template
            The template to calculate.
        action
            Callable to call with results. See above for arguments.
        variables
            Variables to pass to the template.

        Returns
        -------
        Callable to unregister the listener.

        """
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_template, template, action, variables
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_template_result(
        self,
        track_templates: collections.abc.Sequence[TrackTemplate],
        action: TrackTemplateResultListener,
        raise_on_template_error: bool = False,
        strict: bool = False,
        has_super_template: bool = False,
    ) -> _TrackTemplateResultInfo:
        """Add a listener that fires when the result of a template changes.

        The action will fire with the initial result from the template, and
        then whenever the output from the template changes. The template will
        be reevaluated if any states referenced in the last run of the
        template change, or if manually triggered. If the result of the
        evaluation is different from the previous run, the listener is passed
        the result.

        If the template results in an TemplateError, this will be returned to
        the listener the first time this happens but not for subsequent errors.
        Once the template returns to a non-error condition the result is sent
        to the action as usual.

        Parameters
        ----------
        hass
            Home assistant object.
        track_templates
            An iterable of TrackTemplate.
        action
            Callable to call with results.
        raise_on_template_error
            When set to True, if there is an exception
            processing the template during setup, the system
            will raise the exception instead of setting up
            tracking.
        strict
            When set to True, raise on undefined variables.
        has_super_template
            When set to True, the first template will block rendering of other
            templates if it doesn't render as True.

        Returns
        -------
        Info object used to unregister the listener, and refresh the template.

        """
        tracker = _TrackTemplateResultInfo(
            self._shc, track_templates, action, has_super_template
        )
        tracker.async_setup(raise_on_template_error, strict=strict)
        return tracker

    @callback
    def async_track_same_state(
        self,
        period: datetime.timedelta,
        action: collections.abc.Callable[[], collections.abc.Awaitable[None]],
        async_check_same_func: collections.abc.Callable[[str, State, State], bool],
        entity_ids: str | collections.abc.Iterable[str] = Const.MATCH_ALL,
    ) -> CallbackType:
        """Track the state of entities for a period and run an action.

        If async_check_func is None it use the state of orig_value.
        Without entity_ids we track all state changes.
        """
        async_remove_state_for_cancel: CallbackType = None
        async_remove_state_for_listener: CallbackType = None

        job = SmartHomeControllerJob(action)

        @callback
        def clear_listener() -> None:
            """Clear all unsub listener."""
            nonlocal async_remove_state_for_cancel, async_remove_state_for_listener

            if async_remove_state_for_listener is not None:
                async_remove_state_for_listener()
                async_remove_state_for_listener = None
            if async_remove_state_for_cancel is not None:
                async_remove_state_for_cancel()
                async_remove_state_for_cancel = None

        @callback
        def state_for_listener(_now: typing.Any) -> None:
            """Fire on state changes after a delay and calls action."""
            nonlocal async_remove_state_for_listener
            async_remove_state_for_listener = None
            clear_listener()
            self._shc.async_run_shc_job(job)

        @callback
        def state_for_cancel_listener(event: Event) -> None:
            """Fire on changes and cancel for listener if changed."""
            entity: str = event.data["entity_id"]
            from_state: State = event.data.get("old_state")
            to_state: State = event.data.get("new_state")

            if not async_check_same_func(entity, from_state, to_state):
                clear_listener()

        async_remove_state_for_listener = self.async_track_point_in_utc_time(
            state_for_listener, helpers.utcnow() + period
        )

        if entity_ids == Const.MATCH_ALL:
            async_remove_state_for_cancel = self._shc.bus.async_listen(
                Const.EVENT_STATE_CHANGED, state_for_cancel_listener
            )
        else:
            async_remove_state_for_cancel = self.async_track_state_change_event(
                entity_ids,
                state_for_cancel_listener,
            )

        return clear_listener

    def track_same_state(
        self,
        period: datetime.timedelta,
        action: collections.abc.Callable[[], collections.abc.Awaitable[None]],
        async_check_same_func: collections.abc.Callable[[str, State, State], bool],
        entity_ids: str | collections.abc.Iterable[str] = Const.MATCH_ALL,
    ) -> CallbackType:
        """Track the state of entities for a period and run an action.

        If async_check_func is None it use the state of orig_value.
        Without entity_ids we track all state changes.
        """
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_same_state,
            period,
            action,
            async_check_same_func,
            entity_ids,
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_point_in_time(
        self,
        action: SmartHomeControllerJob[collections.abc.Awaitable[None]]
        | collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        point_in_time: datetime.datetime,
    ) -> CallbackType:
        """Add a listener that fires once after a specific point in time."""
        job = (
            action
            if isinstance(action, SmartHomeControllerJob)
            else SmartHomeControllerJob(action)
        )

        @callback
        def utc_converter(utc_now: datetime.datetime) -> None:
            """Convert passed in UTC now to local now."""
            self._shc.async_run_shc_job(job, helpers.as_local(utc_now))

        return self.async_track_point_in_utc_time(utc_converter, point_in_time)

    def track_point_in_time(
        self,
        action: SmartHomeControllerJob[collections.abc.Awaitable[None]]
        | collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        point_in_time: datetime.datetime,
    ) -> CallbackType:
        """Add a listener that fires once after a specific point in time."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_point_in_time, action, point_in_time
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_point_in_utc_time(
        self,
        action: SmartHomeControllerJob[collections.abc.Awaitable[None]]
        | collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        point_in_time: datetime.datetime,
    ) -> CallbackType:
        """Add a listener that fires once after a specific point in UTC time."""
        # Ensure point_in_time is UTC
        utc_point_in_time = helpers.as_utc(point_in_time)

        # Since this is called once, we accept a HassJob so we can avoid
        # having to figure out how to call the action every time its called.
        cancel_callback: asyncio.TimerHandle = None

        @callback
        def run_action(
            job: SmartHomeControllerJob[collections.abc.Awaitable[None]],
        ) -> None:
            """Call the action."""
            nonlocal cancel_callback

            now = EventTracker.time_tracker_utcnow

            # Depending on the available clock support (including timer hardware
            # and the OS kernel) it can happen that we fire a little bit too early
            # as measured by utcnow(). That is bad when callbacks have assumptions
            # about the current time. Thus, we rearm the timer for the remaining
            # time.
            if (delta := (utc_point_in_time - now()).total_seconds()) > 0:
                _LOGGER.debug(f"Called {delta:f} seconds too early, rearming")

                cancel_callback = self._shc.call_later(delta, run_action, job)
                return

            self._shc.async_run_shc_job(job, utc_point_in_time)

        job = (
            action
            if isinstance(action, SmartHomeControllerJob)
            else SmartHomeControllerJob(action)
        )
        delta = utc_point_in_time.timestamp() - time.time()
        cancel_callback = self._shc.call_later(delta, run_action, job)

        @callback
        def unsub_point_in_time_listener() -> None:
            """Cancel the call_later."""
            assert cancel_callback is not None
            cancel_callback.cancel()

        return unsub_point_in_time_listener

    def track_point_in_utc_time(
        self,
        action: SmartHomeControllerJob[collections.abc.Awaitable[None]]
        | collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        point_in_time: datetime.datetime,
    ) -> CallbackType:
        """Add a listener that fires once after a specific point in UTC time."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_point_in_utc_time, action, point_in_time
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_call_later(
        self,
        delay: float | datetime.timedelta,
        action: SmartHomeControllerJob[collections.abc.Awaitable[None]]
        | collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
    ) -> CallbackType:
        """Add a listener that is called in <delay>."""
        if not isinstance(delay, datetime.timedelta):
            delay = datetime.timedelta(seconds=delay)
        return self.async_track_point_in_utc_time(action, helpers.utcnow() + delay)

    def call_later(
        self,
        delay: float | datetime.timedelta,
        action: SmartHomeControllerJob[collections.abc.Awaitable[None]]
        | collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
    ) -> CallbackType:
        """Add a listener that is called in <delay>."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_call_later(delay, action)
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_time_interval(
        self,
        action: collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        interval: datetime.timedelta,
    ) -> CallbackType:
        """Add a listener that fires repetitively at every timedelta interval."""
        remove: CallbackType
        interval_listener_job: SmartHomeControllerJob[None]

        job = SmartHomeControllerJob(action)

        def next_interval() -> datetime.datetime:
            """Return the next interval."""
            return helpers.utcnow() + interval

        @callback
        def interval_listener(now: datetime.datetime) -> None:
            """Handle elapsed intervals."""
            nonlocal remove
            nonlocal interval_listener_job

            remove = self.async_track_point_in_utc_time(
                interval_listener_job, next_interval()
            )
            self._shc.async_run_shc_job(job, now)

        interval_listener_job = SmartHomeControllerJob(interval_listener)
        remove = self.async_track_point_in_utc_time(
            interval_listener_job, next_interval()
        )

        def remove_listener() -> None:
            """Remove interval listener."""
            remove()

        return remove_listener

    def track_time_interval(
        self,
        action: collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        interval: datetime.timedelta,
    ) -> CallbackType:
        """Add a listener that fires repetitively at every timedelta interval."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_time_interval, action, interval
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_sunrise(
        self,
        action: collections.abc.Callable[[], None],
        offset: datetime.timedelta = None,
    ) -> CallbackType:
        """Add a listener that will fire a specified offset from sunrise daily."""
        listener = SunListener(
            self._shc, SmartHomeControllerJob(action), Const.SUN_EVENT_SUNRISE, offset
        )
        listener.async_attach()
        return listener.async_detach

    def track_sunrise(
        self,
        action: collections.abc.Callable[[], None],
        offset: datetime.timedelta = None,
    ) -> CallbackType:
        """Add a listener that will fire a specified offset from sunrise daily."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_sunrise, action, offset
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_sunset(
        self,
        action: collections.abc.Callable[[], None],
        offset: datetime.timedelta = None,
    ) -> CallbackType:
        """Add a listener that will fire a specified offset from sunset daily."""
        listener = SunListener(
            self._shc, SmartHomeControllerJob(action), Const.SUN_EVENT_SUNSET, offset
        )
        listener.async_attach()
        return listener.async_detach

    def track_sunset(
        self,
        action: collections.abc.Callable[[], None],
        offset: datetime.timedelta = None,
    ) -> CallbackType:
        """Add a listener that will fire a specified offset from sunset daily."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_sunset, action, offset
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_utc_time_change(
        self,
        action: collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        hour: typing.Any = None,
        minute: typing.Any = None,
        second: typing.Any = None,
        local: bool = False,
    ) -> CallbackType:
        """Add a listener that will fire if time matches a pattern."""
        # We do not have to wrap the function with time pattern matching logic
        # if no pattern given
        if all(val is None for val in (hour, minute, second)):
            # Previously this relied on EVENT_TIME_FIRED
            # which meant it would not fire right away because
            # the caller would always be misaligned with the call
            # time vs the fire time by < 1s. To preserve this
            # misalignment we use async_track_time_interval here
            return self.async_track_time_interval(action, datetime.timedelta(seconds=1))

        job = SmartHomeControllerJob(action)
        matching_seconds = helpers.parse_time_expression(second, 0, 59)
        matching_minutes = helpers.parse_time_expression(minute, 0, 59)
        matching_hours = helpers.parse_time_expression(hour, 0, 23)

        def calculate_next(now: datetime.datetime) -> datetime.datetime:
            """Calculate and set the next time the trigger should fire."""
            localized_now = helpers.as_local(now) if local else now
            return helpers.find_next_time_expression_time(
                localized_now, matching_seconds, matching_minutes, matching_hours
            )

        time_listener: CallbackType = None

        @callback
        def pattern_time_change_listener(_: datetime.datetime) -> None:
            """Listen for matching time_changed events."""
            nonlocal time_listener

            now = EventTracker.time_tracker_utcnow()
            self._shc.async_run_shc_job(job, helpers.as_local(now) if local else now)

            time_listener = self.async_track_point_in_utc_time(
                pattern_time_change_listener,
                calculate_next(now + datetime.timedelta(seconds=1)),
            )

        time_listener = self.async_track_point_in_utc_time(
            pattern_time_change_listener, calculate_next(helpers.utcnow())
        )

        @callback
        def unsub_pattern_time_change_listener() -> None:
            """Cancel the time listener."""
            assert time_listener is not None
            time_listener()

        return unsub_pattern_time_change_listener

    def track_utc_time_change(
        self,
        action: collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        hour: typing.Any = None,
        minute: typing.Any = None,
        second: typing.Any = None,
        local: bool = False,
    ) -> CallbackType:
        """Listen for matching time_changed events."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_utc_time_change, action, hour, minute, second, local
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    @callback
    def async_track_time_change(
        self,
        action: collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        hour: typing.Any = None,
        minute: typing.Any = None,
        second: typing.Any = None,
    ) -> CallbackType:
        """Add a listener that will fire if local time matches a pattern."""
        return self.async_track_utc_time_change(
            action, hour, minute, second, local=True
        )

    def track_time_change(
        self,
        action: collections.abc.Callable[
            [datetime.datetime], collections.abc.Awaitable[None]
        ],
        hour: typing.Any = None,
        minute: typing.Any = None,
        second: typing.Any = None,
    ) -> CallbackType:
        """Add a listener that will fire if local time matches a pattern."""
        async_remove = self.controller.run_callback_threadsafe(
            self.async_track_time_change, action, hour, minute, second
        ).result()

        def remove() -> None:
            """Threadsafe removal."""
            self.controller.run_callback_threadsafe(async_remove).result()

        return remove

    # For targeted patching in tests
    time_tracker_utcnow = helpers.utcnow


def _async_track_state_added_domain(
    shc: SmartHomeController,
    domains: str | collections.abc.Iterable[str],
    action: collections.abc.Callable[[Event], typing.Any],
) -> CallbackType:
    """async_track_state_added_domain without lowercasing."""
    domain_callbacks = shc.data.setdefault(_TRACK_STATE_ADDED_DOMAIN_CALLBACKS, {})

    if _TRACK_STATE_ADDED_DOMAIN_LISTENER not in shc.data:

        @callback
        def _async_state_change_filter(event: Event) -> bool:
            """Filter state changes by entity_id."""
            return event.data.get("old_state") is None

        @callback
        def _async_state_change_dispatcher(event: Event) -> None:
            """Dispatch state changes by entity_id."""
            if event.data.get("old_state") is not None:
                return

            _async_dispatch_domain_event(shc, event, domain_callbacks)

        shc.data[_TRACK_STATE_ADDED_DOMAIN_LISTENER] = shc.bus.async_listen(
            Const.EVENT_STATE_CHANGED,
            _async_state_change_dispatcher,
            event_filter=_async_state_change_filter,
        )

    job = SmartHomeControllerJob(action)

    for domain in domains:
        domain_callbacks.setdefault(domain, []).append(job)

    @callback
    def remove_listener() -> None:
        """Remove state change listener."""
        _async_remove_indexed_listeners(
            shc,
            _TRACK_STATE_ADDED_DOMAIN_CALLBACKS,
            _TRACK_STATE_ADDED_DOMAIN_LISTENER,
            domains,
            job,
        )

    return remove_listener


@callback
def _async_dispatch_domain_event(
    shc: SmartHomeController,
    event: Event,
    callbacks: dict[str, list[SmartHomeControllerJob[typing.Any]]],
) -> None:
    domain = helpers.split_entity_id(event.data["entity_id"])[0]

    if domain not in callbacks and Const.MATCH_ALL not in callbacks:
        return

    listeners = callbacks.get(domain, []) + callbacks.get(Const.MATCH_ALL, [])

    for job in listeners:
        try:
            shc.async_run_shc_job(job, event)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                f"Error while processing event {event} for domain {domain}"
            )


@callback
def _async_remove_indexed_listeners(
    shc: SmartHomeController,
    data_key: str,
    listener_key: str,
    storage_keys: collections.abc.Iterable[str],
    job: SmartHomeControllerJob[typing.Any],
) -> None:
    """Remove a listener."""
    callbacks = shc.data[data_key]

    for storage_key in storage_keys:
        callbacks[storage_key].remove(job)
        if len(callbacks[storage_key]) == 0:
            del callbacks[storage_key]

    if not callbacks:
        shc.data[listener_key]()
        del shc.data[listener_key]


def _async_track_state_change_event(
    shc: SmartHomeController,
    entity_ids: str | collections.abc.Iterable[str],
    action: collections.abc.Callable[[Event], typing.Any],
) -> CallbackType:
    """async_track_state_change_event without lowercasing."""
    entity_callbacks = shc.data.setdefault(_TRACK_STATE_CHANGE_CALLBACKS, {})

    if _TRACK_STATE_CHANGE_LISTENER not in shc.data:

        @callback
        def _async_state_change_filter(event: Event) -> bool:
            """Filter state changes by entity_id."""
            return event.data.get("entity_id") in entity_callbacks

        @callback
        def _async_state_change_dispatcher(event: Event) -> None:
            """Dispatch state changes by entity_id."""
            entity_id = event.data.get("entity_id")

            if entity_id not in entity_callbacks:
                return

            for job in entity_callbacks[entity_id][:]:
                try:
                    shc.async_run_shc_job(job, event)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(
                        f"Error while processing state change for {entity_id}"
                    )

        shc.data[_TRACK_STATE_CHANGE_LISTENER] = shc.bus.async_listen(
            Const.EVENT_STATE_CHANGED,
            _async_state_change_dispatcher,
            event_filter=_async_state_change_filter,
        )

    job = SmartHomeControllerJob(action)

    for entity_id in entity_ids:
        entity_callbacks.setdefault(entity_id, []).append(job)

    @callback
    def remove_listener() -> None:
        """Remove state change listener."""
        _async_remove_indexed_listeners(
            shc,
            _TRACK_STATE_CHANGE_CALLBACKS,
            _TRACK_STATE_CHANGE_LISTENER,
            entity_ids,
            job,
        )

    return remove_listener


@callback
def _entities_domains_from_render_infos(
    render_infos: collections.abc.Iterable[RenderInfo],
) -> tuple[set[str], set[str]]:
    """Combine from multiple RenderInfo."""
    entities: set[str] = set()
    domains: set[str] = set()

    for render_info in render_infos:
        if render_info.entities:
            entities.update(render_info.entities)
        if render_info.domains:
            domains.update(render_info.domains)
        if render_info.domains_lifecycle:
            domains.update(render_info.domains_lifecycle)
    return entities, domains


@callback
def _render_infos_needs_all_listener(
    render_infos: collections.abc.Iterable[RenderInfo],
) -> bool:
    """Determine if an all listener is needed from RenderInfo."""
    for render_info in render_infos:
        # Tracking all states
        if render_info.all_states or render_info.all_states_lifecycle:
            return True

        # Previous call had an exception
        # so we do not know which states
        # to track
        if render_info.exception:
            return True

    return False


@callback
def _render_infos_to_track_states(
    render_infos: collections.abc.Iterable[RenderInfo],
) -> TrackStates:
    """Create a TrackStates dataclass from the latest RenderInfo."""
    if _render_infos_needs_all_listener(render_infos):
        return TrackStates(True, set(), set())

    return TrackStates(False, *_entities_domains_from_render_infos(render_infos))


@callback
def _event_triggers_rerender(event: Event, info: RenderInfo) -> bool:
    """Determine if a template should be re-rendered from an event."""
    entity_id = typing.cast(str, event.data.get(Const.ATTR_ENTITY_ID))

    if info.filter(entity_id):
        return True

    if (
        event.data.get("new_state") is not None
        and event.data.get("old_state") is not None
    ):
        return False

    return bool(info.filter_lifecycle(entity_id))


@callback
def _rate_limit_for_event(
    event: Event, info: RenderInfo, track_template_: TrackTemplate
) -> datetime.timedelta:
    """Determine the rate limit for an event."""
    # Specifically referenced entities are excluded
    # from the rate limit
    if event.data.get(Const.ATTR_ENTITY_ID) in info.entities:
        return None

    if track_template_.rate_limit is not None:
        return track_template_.rate_limit

    rate_limit: datetime.timedelta = info.rate_limit
    return rate_limit


def _suppress_domain_all_in_render_info(render_info: RenderInfo) -> RenderInfo:
    """Remove the domains and all_states from render info during a ratelimit."""
    # pylint: disable=protected-access
    rate_limited_render_info = copy.copy(render_info)
    rate_limited_render_info._all_states = False
    rate_limited_render_info._all_states_lifecycle = False
    rate_limited_render_info._domains = set()
    rate_limited_render_info._domains_lifecycle = set()
    return rate_limited_render_info


def _process_state_match(
    parameter: str | collections.abc.Iterable[str], invert: bool = False
) -> collections.abc.Callable[[str], bool]:
    """Convert parameter to function that matches input against parameter."""
    if parameter is None or parameter == Const.MATCH_ALL:
        return lambda _: not invert

    if isinstance(parameter, str) or not hasattr(parameter, "__iter__"):
        return lambda state: invert is not (state == parameter)

    parameter_set = set(parameter)
    return lambda state: invert is not (state in parameter_set)


@callback
def _async_string_to_lower_list(
    instr: str | collections.abc.Iterable[str],
) -> list[str]:
    if isinstance(instr, str):
        return [instr.lower()]

    return [mstr.lower() for mstr in instr]


@callback
def _remove_empty_listener() -> None:
    """Remove a listener that does nothing."""
