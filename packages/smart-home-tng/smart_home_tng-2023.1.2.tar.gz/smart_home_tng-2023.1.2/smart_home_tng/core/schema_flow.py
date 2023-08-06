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

# pylint: disable=unused-variable

import abc
import copy
import dataclasses
import types
import typing

import voluptuous as vol

from . import helpers
from .callback import callback
from .config_entry import ConfigEntry
from .config_flow import ConfigFlow
from .entity_selector import EntitySelector
from .entity_selector_config import EntitySelectorConfig
from .flow_result import FlowResult
from .options_flow import OptionsFlow
from .unknown_handler import UnknownHandler

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


class _Error(Exception):
    """Validation failed."""


class _ConfigFlow:
    pass


class _OptionsFlow:
    pass


@dataclasses.dataclass
class _FormStep:
    """Define a config or options flow step."""

    # Optional schema for requesting and validating user input. If schema validation
    # fails, the step will be retried. If the schema is None, no user input is requested.
    schema: vol.Schema | typing.Callable[
        [_ConfigFlow | _OptionsFlow, dict[str, typing.Any]],
        vol.Schema,
    ] | None

    # Optional function to validate user input.
    # The validate_user_input function is called if the schema validates successfully.
    # The validate_user_input function is passed the user input from the current step.
    # The validate_user_input should raise SchemaFlowError is user input is invalid.
    validate_user_input: typing.Callable[
        [dict[str, typing.Any]], dict[str, typing.Any]
    ] = lambda x: x

    # Optional function to identify next step.
    # The next_step function is called if the schema validates successfully or if no
    # schema is defined. The next_step function is passed the union of config entry
    # options and user input from previous steps.
    # If next_step returns None, the flow is ended with FlowResultType.CREATE_ENTRY.
    next_step: typing.Callable[[dict[str, typing.Any]], str] = lambda _: None

    # Optional function to allow amending a form schema.
    # The update_form_schema function is called before async_show_form is called. The
    # update_form_schema function is passed the handler, which is either an instance of
    # SchemaConfigFlowHandler or SchemaOptionsFlowHandler, the schema, and the union of
    # config entry options and user input from previous steps.
    update_form_schema: typing.Callable[
        [
            _ConfigFlow | _OptionsFlow,
            vol.Schema,
            dict[str, typing.Any],
        ],
        vol.Schema,
    ] = lambda _handler, schema, _options: schema


@dataclasses.dataclass
class _MenuStep:
    """Define a config or options flow menu step."""

    # Menu options
    options: list[str] | dict[str, str]


class _ConfigFlow(ConfigFlow):
    """Handle a schema based config flow."""

    config_flow: dict[str, _FormStep | _MenuStep]
    options_flow: dict[str, _FormStep | _MenuStep] = None

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Initialize a subclass."""
        super().__init_subclass__(**kwargs)

        @callback
        def _async_get_options_flow(
            self: cls,
            config_entry: ConfigEntry,
        ) -> OptionsFlow:
            """Get the options flow for this handler."""
            if cls.options_flow is None:
                raise UnknownHandler

            return _OptionsFlow(
                self.controller,
                config_entry,
                cls.options_flow,
                cls.async_options_flow_finished,
            )

        # Create an async_get_options_flow method
        cls.async_get_options_flow = _async_get_options_flow  # type: ignore[assignment]

        # Create flow step methods for each step defined in the flow schema
        for step in cls.config_flow:
            setattr(cls, f"async_step_{step}", cls._async_step(step))

    def __init__(
        self,
        shc: SmartHomeController,
        handler: str,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
        version: int = 1,
    ) -> None:
        """Initialize config flow."""
        super().__init__(shc, handler, context, data, version)
        self._common_handler = _CommonFlowHandler(self, self.config_flow, None)

    @classmethod
    @callback
    def supports_options_flow(cls, _config_entry: ConfigEntry) -> bool:
        """Return options flow support for this handler."""
        return cls.options_flow is not None

    @staticmethod
    def _async_step(step_id: str) -> typing.Callable:
        """Generate a step handler."""

        async def _async_step(
            self: _ConfigFlow, user_input: dict[str, typing.Any] = None
        ) -> FlowResult:
            """Handle a config flow step."""
            # pylint: disable-next=protected-access
            result = await self._common_handler.async_step(step_id, user_input)
            return result

        return _async_step

    @abc.abstractmethod
    @callback
    def async_config_entry_title(self, options: typing.Mapping[str, typing.Any]) -> str:
        """Return config entry title.

        The options parameter contains config entry options, which is the union of user
        input from the config flow steps.
        """

    @callback
    def async_config_flow_finished(
        self, options: typing.Mapping[str, typing.Any]
    ) -> None:
        """Take necessary actions after the config flow is finished, if needed.

        The options parameter contains config entry options, which is the union of user
        input from the config flow steps.
        """

    @callback
    @staticmethod
    def async_options_flow_finished(
        shc: SmartHomeController, options: typing.Mapping[str, typing.Any]
    ) -> None:
        """Take necessary actions after the options flow is finished, if needed.

        The options parameter contains config entry options, which is the union of stored
        options and user input from the options flow steps.
        """

    @callback
    def async_create_entry(  # pylint: disable=arguments-differ
        self,
        data: typing.Mapping[str, typing.Any],
        **kwargs: typing.Any,
    ) -> FlowResult:
        """Finish config flow and create a config entry."""
        self.async_config_flow_finished(data)
        return super().async_create_entry(
            data={}, options=data, title=self.async_config_entry_title(data), **kwargs
        )


class _CommonFlowHandler:
    """Handle a schema based config or options flow."""

    def __init__(
        self,
        handler: _ConfigFlow | _OptionsFlow,
        flow: dict[str, _FormStep | _MenuStep],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize a common handler."""
        self._flow = flow
        self._handler = handler
        self._options = dict(config_entry.options) if config_entry is not None else {}

    async def async_step(
        self, step_id: str, user_input: dict[str, typing.Any] | None = None
    ) -> FlowResult:
        """Handle a step."""
        if isinstance(self._flow[step_id], _FormStep):
            return await self._async_form_step(step_id, user_input)
        return await self._async_menu_step(step_id, user_input)

    def _get_schema(
        self, form_step: _FormStep, options: dict[str, typing.Any]
    ) -> vol.Schema:
        if form_step.schema is None:
            return None
        if isinstance(form_step.schema, vol.Schema):
            return form_step.schema
        return form_step.schema(self._handler, options)

    async def _async_form_step(
        self, step_id: str, user_input: dict[str, typing.Any] = None
    ) -> FlowResult:
        """Handle a form step."""
        form_step: _FormStep = typing.cast(_FormStep, self._flow[step_id])

        if (
            user_input is not None
            and (data_schema := self._get_schema(form_step, self._options))
            and data_schema.schema
            and not self._handler.show_advanced_options
        ):
            # Add advanced field default if not set
            for key in data_schema.schema.keys():
                if isinstance(key, (vol.Optional, vol.Required)):
                    if (
                        key.description
                        and key.description.get("advanced")
                        and key.default is not vol.UNDEFINED
                        and key not in self._options
                    ):
                        user_input[str(key.schema)] = key.default()

        if user_input is not None and form_step.schema is not None:
            # Do extra validation of user input
            try:
                user_input = form_step.validate_user_input(user_input)
            except _Error as exc:
                return self._show_next_step(step_id, exc, user_input)

        if user_input is not None:
            # User input was validated successfully, update options
            self._options.update(user_input)

        next_step_id: str = step_id
        if form_step.next_step and (user_input is not None or form_step.schema is None):
            # Get next step
            next_step_id_or_end_flow = form_step.next_step(self._options)
            if next_step_id_or_end_flow is None:
                # Flow done, create entry or update config entry options
                return self._handler.async_create_entry(data=self._options)

            next_step_id = next_step_id_or_end_flow

        return self._show_next_step(next_step_id)

    def _show_next_step(
        self,
        next_step_id: str,
        error: _Error = None,
        user_input: dict[str, typing.Any] = None,
    ) -> FlowResult:
        """Show form for next step."""
        form_step: _FormStep = typing.cast(_FormStep, self._flow[next_step_id])

        options = dict(self._options)
        if user_input:
            options.update(user_input)

        if (
            data_schema := self._get_schema(form_step, self._options)
        ) and data_schema.schema:
            # Make a copy of the schema with suggested values set to saved options
            schema = {}
            for key, val in data_schema.schema.items():
                if isinstance(key, vol.Marker):
                    # Exclude advanced field
                    if (
                        key.description
                        and key.description.get("advanced")
                        and not self._handler.show_advanced_options
                    ):
                        continue

                new_key = key
                if key in options and isinstance(key, vol.Marker):
                    # Copy the marker to not modify the flow schema
                    new_key = copy.copy(key)
                    new_key.description = {"suggested_value": options[key]}
                schema[new_key] = val
            data_schema = vol.Schema(schema)

        errors = {"base": str(error)} if error else None

        # Show form for next step
        return self._handler.async_show_form(
            step_id=next_step_id, data_schema=data_schema, errors=errors
        )

    async def _async_menu_step(
        self, step_id: str, _user_input: dict[str, typing.Any] = None
    ) -> FlowResult:
        """Handle a menu step."""
        form_step: _MenuStep = typing.cast(_MenuStep, self._flow[step_id])
        return self._handler.async_show_menu(
            step_id=step_id,
            menu_options=form_step.options,
        )


class _OptionsFlow(OptionsFlow):
    """Handle a schema based options flow."""

    def __init__(
        self,
        shc: SmartHomeController,
        config_entry: ConfigEntry,
        options_flow: dict[str, vol.Schema],
        async_options_flow_finished: typing.Callable[
            [SmartHomeController, typing.Mapping[str, typing.Any]], None
        ],
    ) -> None:
        """Initialize options flow."""
        super().__init__(None)
        self._common_handler = _CommonFlowHandler(self, options_flow, config_entry)
        self._config_entry = config_entry
        self._async_options_flow_finished = async_options_flow_finished
        self._shc = shc

        for step in options_flow:
            setattr(
                self,
                f"async_step_{step}",
                types.MethodType(self._async_step(step), self),
            )

    @property
    def config_entry(self) -> ConfigEntry:
        return self._config_entry

    @staticmethod
    def _async_step(step_id: str) -> typing.Callable:
        """Generate a step handler."""

        async def _async_step(
            self: _OptionsFlow, user_input: dict[str, typing.Any] = None
        ) -> FlowResult:
            """Handle an options flow step."""
            # pylint: disable-next=protected-access
            result = await self._common_handler.async_step(step_id, user_input)
            return result

        return _async_step

    @callback
    def async_create_entry(  # pylint: disable=arguments-differ
        self,
        data: typing.Mapping[str, typing.Any],
        **kwargs: typing.Any,
    ) -> FlowResult:
        """Finish config flow and create a config entry."""
        self._async_options_flow_finished(self._shc, data)
        return super().async_create_entry(title="", data=data, **kwargs)


# pylint: disable=invalid-name
class SchemaFlow:
    """SchemaFlow namespace."""

    Error: typing.TypeAlias = _Error

    FormStep: typing.Final = _FormStep
    MenuStep: typing.Final = _MenuStep

    ConfigFlow: typing.TypeAlias = _ConfigFlow
    OptionsFlow: typing.TypeAlias = _OptionsFlow

    @staticmethod
    @callback
    def wrapped_entity_config_entry_title(
        shc: SmartHomeController, entity_id_or_uuid: str
    ) -> str:
        """Generate title for a config entry wrapping a single entity.

        If the entity is registered, use the registry entry's name.
        If the entity is in the state machine, use the name from the state.
        Otherwise, fall back to the object ID.
        """
        registry = shc.entity_registry
        entity_id = registry.async_validate_entity_id(entity_id_or_uuid)
        object_id = helpers.split_entity_id(entity_id)[1]
        entry = registry.async_get(entity_id)
        if entry:
            return entry.name or entry.original_name or object_id
        state = shc.states.get(entity_id)
        if state:
            return state.name or object_id
        return object_id

    @staticmethod
    @callback
    def entity_selector_without_own_entities(
        shc: SmartHomeController,
        handler: _OptionsFlow,
        entity_selector_config: EntitySelectorConfig,
    ) -> vol.Schema:
        """Return an entity selector which excludes own entities."""
        entity_registry = shc.entity_registry
        entities = entity_registry.async_entries_for_config_entry(
            handler.config_entry.entry_id,
        )
        entity_ids = [ent.entity_id for ent in entities]

        final_selector_config = entity_selector_config.copy()
        final_selector_config["exclude_entities"] = entity_ids

        return EntitySelector(final_selector_config)
