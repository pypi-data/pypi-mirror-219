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

import datetime as dt
import logging
import typing
import voluptuous as vol

from .callback import callback
from .callback_type import CallbackType
from .condition_error import ConditionError
from .config_type import ConfigType
from .config_validation import ConfigValidation as _cv
from .const import Const
from .event import Event
from .platform import Platform
from .script_condition import ScriptCondition
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_job import SmartHomeControllerJob
from .state import State
from .template import Template
from .template_error import TemplateError
from .trigger_action_type import TriggerActionType
from .trigger_info import TriggerInfo
from .trigger_platform import TriggerPlatform


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class Trigger:
    """Trigger namespace."""

    _default_impl: TriggerPlatform = None

    CONF_PLATFORM: typing.Final = Const.CONF_PLATFORM

    CONF_HOURS: typing.Final = "hours"
    CONF_MINUTES: typing.Final = "minutes"
    CONF_SECONDS: typing.Final = "seconds"

    CONF_EVENT: typing.Final = Const.CONF_EVENT
    CONF_EVENT_TYPE: typing.Final = "event_type"
    CONF_EVENT_DATA: typing.Final = Const.CONF_EVENT_DATA
    CONF_EVENT_CONTEXT: typing.Final = "context"

    EVENT_TRIGGER_SCHEMA: typing.Final = _cv.TRIGGER_BASE_SCHEMA.extend(
        {
            vol.Required(Const.CONF_PLATFORM): CONF_EVENT,
            vol.Required(CONF_EVENT_TYPE): vol.All(_cv.ensure_list, [_cv.template]),
            vol.Optional(CONF_EVENT_DATA): vol.All(dict, _cv.template_complex),
            vol.Optional(CONF_EVENT_CONTEXT): vol.All(dict, _cv.template_complex),
        }
    )

    @staticmethod
    def _get_core() -> TriggerPlatform:
        """Return core (default) implementation."""
        if Trigger._default_impl is None:
            comp = SmartHomeControllerComponent.get_component(Const.CORE_COMPONENT_NAME)
            if comp is not None:
                impl = comp.get_platform(Platform.TRIGGER)
                if isinstance(impl, TriggerPlatform):
                    Trigger._default_impl = impl
        return Trigger._default_impl

    @staticmethod
    async def async_validate_trigger_config(config: ConfigType) -> ConfigType:
        """Validate trigger configuration."""
        if core_impl := Trigger._get_core():
            return await core_impl.async_validate_trigger_config(config)
        return config

    @staticmethod
    async def async_attach_trigger(
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
    ) -> CallbackType:
        """Attach a trigger."""
        if core_impl := Trigger._get_core():
            return await core_impl.async_attach_trigger(config, action, trigger_info)
        return None

    @staticmethod
    async def async_attach_state_trigger(
        shc: SmartHomeController,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
        platform_type="state",
    ) -> CallbackType:
        """Listen for state changes based on configuration."""
        entity_ids = config[Const.CONF_ENTITY_ID]

        tracker = shc.tracker

        if (from_state := config.get(Const.CONF_FROM)) is not None:
            match_from_state = tracker.process_state_match(from_state)
        elif (not_from_state := config.get(Const.CONF_NOT_FROM)) is not None:
            match_from_state = tracker.process_state_match(not_from_state, invert=True)
        else:
            match_from_state = tracker.process_state_match(Const.MATCH_ALL)

        if (to_state := config.get(Const.CONF_TO)) is not None:
            match_to_state = tracker.process_state_match(to_state)
        elif (not_to_state := config.get(Const.CONF_NOT_TO)) is not None:
            match_to_state = tracker.process_state_match(not_to_state, invert=True)
        else:
            match_to_state = tracker.process_state_match(Const.MATCH_ALL)

        time_delta = config.get(Const.CONF_FOR)
        Template.attach(shc, time_delta)
        # If neither CONF_FROM or CONF_TO are specified,
        # fire on all changes to the state or an attribute
        match_all = all(
            item not in config
            for item in (
                Const.CONF_FROM,
                Const.CONF_NOT_FROM,
                Const.CONF_NOT_TO,
                Const.CONF_TO,
            )
        )
        unsub_track_same = {}
        period: dict[str, dt.timedelta] = {}
        attribute = config.get(Const.CONF_ATTRIBUTE)
        job = SmartHomeControllerJob(action)

        trigger_data = trigger_info["trigger_data"]
        _variables = trigger_info["variables"] or {}

        @callback
        def state_automation_listener(event: Event):
            """Listen for state changes and calls action."""
            entity: str = event.data["entity_id"]
            from_s: State = event.data.get("old_state")
            to_s: State = event.data.get("new_state")

            if from_s is None:
                old_value = None
            elif attribute is None:
                old_value = from_s.state
            else:
                old_value = from_s.attributes.get(attribute)

            if to_s is None:
                new_value = None
            elif attribute is None:
                new_value = to_s.state
            else:
                new_value = to_s.attributes.get(attribute)

            # When we listen for state changes with `match_all`, we
            # will trigger even if just an attribute changes. When
            # we listen to just an attribute, we should ignore all
            # other attribute changes.
            if attribute is not None and old_value == new_value:
                return

            if (
                not match_from_state(old_value)
                or not match_to_state(new_value)
                or (not match_all and old_value == new_value)
            ):
                return

            @callback
            def call_action():
                """Call action with right context."""
                shc.async_run_shc_job(
                    job,
                    {
                        "trigger": {
                            **trigger_data,
                            "platform": platform_type,
                            "entity_id": entity,
                            "from_state": from_s,
                            "to_state": to_s,
                            "for": time_delta if not time_delta else period[entity],
                            "attribute": attribute,
                            "description": f"state of {entity}",
                        }
                    },
                    event.context,
                )

            if not time_delta:
                call_action()
                return

            info = {
                "trigger": {
                    "platform": platform_type,
                    "entity_id": entity,
                    "from_state": from_s,
                    "to_state": to_s,
                }
            }
            variables = {**_variables, **info}

            try:
                period[entity] = _cv.positive_time_period(
                    Template.render_complex(time_delta, variables)
                )
            except (TemplateError, vol.Invalid) as ex:
                _LOGGER.error(
                    f"Error rendering '{trigger_info['name']}' for template: " + f"{ex}"
                )
                return

            def _check_same_state(_, _2, new_st: State) -> bool:
                if new_st is None:
                    return False

                cur_value: str | None
                if attribute is None:
                    cur_value = new_st.state
                else:
                    cur_value = new_st.attributes.get(attribute)

                if Const.CONF_FROM in config and Const.CONF_TO not in config:
                    return cur_value != old_value

                return cur_value == new_value

            unsub_track_same[entity] = tracker.async_track_same_state(
                period[entity],
                call_action,
                _check_same_state,
                entity_ids=entity,
            )

        unsub = tracker.async_track_state_change_event(
            entity_ids, state_automation_listener
        )

        @callback
        def async_remove():
            """Remove state listeners async."""
            unsub()
            for async_remove in unsub_track_same.values():
                async_remove()
            unsub_track_same.clear()

        return async_remove

    @staticmethod
    async def async_attach_numeric_state_trigger(
        shc: SmartHomeController,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
        platform_type="numeric_state",
    ) -> CallbackType:
        """Listen for state changes based on configuration."""
        entity_ids: list[str] = config[Const.CONF_ENTITY_ID]
        below = config.get(Const.CONF_BELOW)
        above = config.get(Const.CONF_ABOVE)
        time_delta = config.get(Const.CONF_FOR)
        Template.attach(shc, time_delta)
        value_template = config.get(Const.CONF_VALUE_TEMPLATE)
        unsub_track_same = {}
        armed_entities = set()
        period: dict = {}
        attribute = config.get(Const.CONF_ATTRIBUTE)
        job = SmartHomeControllerJob(action)

        trigger_data = trigger_info["trigger_data"]
        _variables = trigger_info["variables"] or {}

        if value_template is not None:
            value_template.controller = shc

        def variables(entity_id):
            """Return a dict with trigger variables."""
            info = {
                "trigger": {
                    "platform": platform_type,
                    "entity_id": entity_id,
                    "below": below,
                    "above": above,
                    "attribute": attribute,
                }
            }
            return {**_variables, **info}

        @callback
        def check_numeric_state(entity_id, _from_s, to_s):
            """Return whether the criteria are met, raise ConditionError if unknown."""
            condition: ScriptCondition = ScriptCondition.get_action_condition_protocol(
                shc
            )
            return condition.async_numeric_state(
                to_s, below, above, value_template, variables(entity_id), attribute
            )

        # Each entity that starts outside the range is already armed (ready to fire).
        for entity_id in entity_ids:
            try:
                if not check_numeric_state(entity_id, None, entity_id):
                    armed_entities.add(entity_id)
            except ConditionError as ex:
                _LOGGER.warning(
                    f"Error initializing '{trigger_info['name']}' trigger: " + f"{ex}",
                )

        @callback
        def state_automation_listener(event):
            """Listen for state changes and calls action."""
            entity_id = event.data.get("entity_id")
            from_s = event.data.get("old_state")
            to_s = event.data.get("new_state")

            @callback
            def call_action():
                """Call action with right context."""
                shc.async_run_shc_job(
                    job,
                    {
                        "trigger": {
                            **trigger_data,
                            "platform": platform_type,
                            "entity_id": entity_id,
                            "below": below,
                            "above": above,
                            "from_state": from_s,
                            "to_state": to_s,
                            "for": time_delta if not time_delta else period[entity_id],
                            "description": f"numeric state of {entity_id}",
                        }
                    },
                    to_s.context,
                )

            @callback
            def check_numeric_state_no_raise(entity_id, from_s, to_s):
                """Return True if the criteria are now met, False otherwise."""
                try:
                    return check_numeric_state(entity_id, from_s, to_s)
                except ConditionError:
                    # This is an internal same-state listener so we just drop the
                    # error. The same error will be reached and logged by the
                    # primary async_track_state_change_event() listener.
                    return False

            try:
                matching = check_numeric_state(entity_id, from_s, to_s)
            except ConditionError as ex:
                _LOGGER.warning(
                    f"Error in '{trigger_info['name']}' trigger: " + f"{ex}"
                )
                return

            if not matching:
                armed_entities.add(entity_id)
            elif entity_id in armed_entities:
                armed_entities.discard(entity_id)

                if time_delta:
                    try:
                        period[entity_id] = _cv.positive_time_period(
                            Template.render_complex(time_delta, variables(entity_id))
                        )
                    except (TemplateError, vol.Invalid) as ex:
                        _LOGGER.error(
                            f"Error rendering '{trigger_info['name']}' for template: "
                            + f"{ex}",
                        )
                        return

                    unsub_track_same[entity_id] = shc.tracker.async_track_same_state(
                        period[entity_id],
                        call_action,
                        entity_ids=entity_id,
                        async_check_same_func=check_numeric_state_no_raise,
                    )
                else:
                    call_action()

        unsub = shc.tracker.async_track_state_change_event(
            entity_ids, state_automation_listener
        )

        @callback
        def async_remove():
            """Remove state listeners async."""
            unsub()
            for async_remove in unsub_track_same.values():
                async_remove()
            unsub_track_same.clear()

        return async_remove

    @staticmethod
    async def async_attach_event_trigger(
        shc: SmartHomeController,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
        platform_type="event",
    ) -> CallbackType:
        """Listen for events based on configuration."""
        trigger_data = trigger_info["trigger_data"]
        variables = trigger_info["variables"]

        Template.attach(shc, config[Trigger.CONF_EVENT_TYPE])
        event_types = Template.render_complex(
            config[Trigger.CONF_EVENT_TYPE], variables, limited=True
        )
        removes = []

        event_data_schema = None
        if Trigger.CONF_EVENT_DATA in config:
            # Render the schema input
            Template.attach(shc, config[Trigger.CONF_EVENT_DATA])
            event_data = {}
            event_data.update(
                Template.render_complex(
                    config[Trigger.CONF_EVENT_DATA], variables, limited=True
                )
            )
            # Build the schema
            event_data_schema = vol.Schema(
                {vol.Required(key): value for key, value in event_data.items()},
                extra=vol.ALLOW_EXTRA,
            )

        event_context_schema = None
        if Trigger.CONF_EVENT_CONTEXT in config:
            # Render the schema input
            Template.attach(shc, config[Trigger.CONF_EVENT_CONTEXT])
            event_context = {}
            event_context.update(
                Template.render_complex(
                    config[Trigger.CONF_EVENT_CONTEXT], variables, limited=True
                )
            )
            # Build the schema
            event_context_schema = vol.Schema(
                {
                    vol.Required(key): _schema_value(value)
                    for key, value in event_context.items()
                },
                extra=vol.ALLOW_EXTRA,
            )

        job = SmartHomeControllerJob(action)

        @callback
        def handle_event(event: Event) -> None:
            """Listen for events and calls the action when data matches."""
            try:
                # Check that the event data and context match the configured
                # schema if one was provided
                if event_data_schema:
                    event_data_schema(event.data)
                if event_context_schema:
                    event_context_schema(event.context.as_dict())
            except vol.Invalid:
                # If event doesn't match, skip event
                return

            shc.async_run_shc_job(
                job,
                {
                    "trigger": {
                        **trigger_data,
                        "platform": platform_type,
                        "event": event,
                        "description": f"event '{event.event_type}'",
                    }
                },
                event.context,
            )

        removes = [
            shc.bus.async_listen(event_type, handle_event) for event_type in event_types
        ]

        @callback
        def remove_listen_events() -> None:
            """Remove event listeners."""
            for remove in removes:
                remove()

        return remove_listen_events


def _schema_value(value: typing.Any) -> typing.Any:
    if isinstance(value, list):
        return vol.In(value)

    return value
