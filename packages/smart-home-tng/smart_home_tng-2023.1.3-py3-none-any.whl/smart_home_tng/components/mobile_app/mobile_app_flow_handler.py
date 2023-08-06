"""
Mobile App Component for Smart Home - The Next Generation.

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
import uuid

from ... import core
from .const import Const


# pylint: disable=unused-variable
class MobileAppFlowHandler(core.ConfigFlow):
    """Handle a Mobile App config flow."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        version = 1
        super().__init__(owner.controller, owner.domain, context, data, version)
        self._owner = owner

    async def async_step_user(self, _user_input=None):
        """Handle a flow initialized by the user."""
        placeholders = {
            "apps_url": "https://www.home-assistant.io/integrations/mobile_app/#apps"
        }

        return self.async_abort(
            reason="install_app", description_placeholders=placeholders
        )

    async def async_step_registration(self, user_input=None):
        """Handle a flow initialized during registration."""
        if core.Const.ATTR_DEVICE_ID in user_input:
            # Unique ID is combi of app + device ID.
            await self.async_set_unique_id(
                f"{user_input[Const.ATTR_APP_ID]}-{user_input[core.Const.ATTR_DEVICE_ID]}"
            )
        else:
            user_input[core.Const.ATTR_DEVICE_ID] = str(uuid.uuid4()).replace("-", "")

        # Register device tracker entity and add to person registering app
        entity_registry = self._shc.entity_registry
        devt_entry = entity_registry.async_get_or_create(
            "device_tracker",
            self._owner.domain,
            user_input[core.Const.ATTR_DEVICE_ID],
            suggested_object_id=user_input[Const.ATTR_DEVICE_NAME],
        )
        person = self._owner.get_component(core.Const.PERSON_COMPONENT_NAME)
        if isinstance(person, core.PersonComponent):
            await person.async_add_user_device_tracker(
                user_input[Const.CONF_USER_ID], devt_entry.entity_id
            )

        return self.async_create_entry(
            title=user_input[Const.ATTR_DEVICE_NAME], data=user_input
        )
