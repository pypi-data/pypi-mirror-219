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


import collections.abc
import types
import typing

import voluptuous as vol

from . import helpers
from .callback import callback
from .flow_result import FlowResult
from .flow_result_type import FlowResultType


# pylint: disable=unused-variable
class FlowHandler:
    """Handle the configuration flow of a component."""

    # Event that is fired when a flow is progressed via external or progress source.
    EVENT_DATA_ENTRY_FLOW_PROGRESSED: typing.Final = "data_entry_flow_progressed"

    def __init__(
        self,
        handler: typing.Any,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
        version: int = 1,
    ):
        # Set by flow manager
        self._cur_step: dict[str, typing.Any] = None
        # While not purely typed, it makes typehinting more useful for us
        # and removes the need for constant None checks or asserts.
        self._flow_id: str = helpers.random_uuid_hex()
        self._handler = handler
        # Ensure the attribute has a subscriptable, but immutable, default value.
        if context is None:
            self._context: dict[str, typing.Any] = types.MappingProxyType({})
        else:
            self._context = context

        init_step = self.context.get("source", None)
        if init_step is not None:
            self._init_step = str(init_step)
        else:
            # Set by _async_create_flow callback
            self._init_step = "init"

        # The initial data that was used to start the flow
        self._init_data: typing.Any = data

        # Set by developer
        self._version = version

    @property
    def context(self) -> dict[str, typing.Any]:
        return self._context

    @property
    def flow_id(self) -> str:
        return self._flow_id

    @property
    def handler(self) -> typing.Any:
        return self._handler

    @property
    def init_data(self) -> typing.Any:
        return self._init_data

    @init_data.setter
    def init_data(self, value: typing.Any) -> None:
        if self._init_data is None:
            self._init_data = value

    @property
    def cur_step(self) -> dict[str, typing.Any]:
        return self._cur_step

    @property
    def version(self) -> int:
        return self._version

    @property
    def init_step(self) -> str:
        return self._init_step

    @init_step.setter
    def init_step(self, value: str) -> None:
        if self._init_step == "init":
            self._init_step = value

    @property
    def source(self) -> str:
        """Source that initialized the flow."""
        return self._context.get("source", None)

    @property
    def show_advanced_options(self) -> bool:
        """If we should show advanced options."""
        return self._context.get("show_advanced_options", False)

    def set_result(self, result: FlowResult) -> None:
        self._cur_step = result

    @callback
    def async_show_form(
        self,
        *,
        step_id: str,
        data_schema: vol.Schema = None,
        errors: dict[str, str] = None,
        description_placeholders: dict[str, typing.Any] = None,
        last_step: bool = None,
    ) -> FlowResult:
        """Return the definition of a form to gather user input."""
        return {
            "type": FlowResultType.FORM,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "step_id": step_id,
            "data_schema": data_schema,
            "errors": errors,
            "description_placeholders": description_placeholders,
            "last_step": last_step,  # Display next or submit button in frontend
        }

    @callback
    def async_create_entry(
        self,
        *,
        title: str,
        data: collections.abc.Mapping[str, typing.Any],
        description: str = None,
        description_placeholders: dict = None,
    ) -> FlowResult:
        """Finish config flow and create a config entry."""
        return {
            "version": self._version,
            "type": FlowResultType.CREATE_ENTRY,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "title": title,
            "data": data,
            "description": description,
            "description_placeholders": description_placeholders,
        }

    @callback
    def async_abort(
        self, *, reason: str, description_placeholders: dict = None
    ) -> FlowResult:
        """Abort the config flow."""
        return self.create_abort_data(reason, description_placeholders)

    @callback
    def create_abort_data(
        self,
        reason: str,
        description_placeholders: dict = None,
    ) -> FlowResult:
        """Return the definition of an external step for the user to take."""
        return {
            "type": FlowResultType.ABORT,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "reason": reason,
            "description_placeholders": description_placeholders,
        }

    @callback
    def async_external_step(
        self, *, step_id: str, url: str, description_placeholders: dict = None
    ) -> FlowResult:
        """Return the definition of an external step for the user to take."""
        return {
            "type": FlowResultType.EXTERNAL,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "step_id": step_id,
            "url": url,
            "description_placeholders": description_placeholders,
        }

    @callback
    def async_external_step_done(self, *, next_step_id: str) -> FlowResult:
        """Return the definition of an external step for the user to take."""
        return {
            "type": FlowResultType.EXTERNAL_DONE,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "step_id": next_step_id,
        }

    @callback
    def async_show_progress(
        self,
        *,
        step_id: str,
        progress_action: str,
        description_placeholders: dict = None,
    ) -> FlowResult:
        """Show a progress message to the user, without user input allowed."""
        return {
            "type": FlowResultType.SHOW_PROGRESS,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "step_id": step_id,
            "progress_action": progress_action,
            "description_placeholders": description_placeholders,
        }

    @callback
    def async_show_progress_done(self, *, next_step_id: str) -> FlowResult:
        """Mark the progress done."""
        return {
            "type": FlowResultType.SHOW_PROGRESS_DONE,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "step_id": next_step_id,
        }

    @callback
    def async_show_menu(
        self,
        *,
        step_id: str,
        menu_options: list[str] | dict[str, str],
        description_placeholders: dict = None,
    ) -> FlowResult:
        """Show a navigation menu to the user.

        Options dict maps step_id => i18n label
        """
        return {
            "type": FlowResultType.MENU,
            "flow_id": self._flow_id,
            "handler": self._handler,
            "step_id": step_id,
            "data_schema": vol.Schema({"next_step_id": vol.In(menu_options)}),
            "menu_options": menu_options,
            "description_placeholders": description_placeholders,
        }
