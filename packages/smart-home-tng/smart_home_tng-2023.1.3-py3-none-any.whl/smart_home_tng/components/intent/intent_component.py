"""
Intent Component for Smart Home - The Next Generation.

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
from .intent_handle_view import IntentHandleView

_const: typing.TypeAlias = core.Const
_intent: typing.TypeAlias = core.Intent


# pylint: disable=unused-variable
class IntentComponent(core.SmartHomeControllerComponent):
    """The Intent integration."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Intent component."""
        if not await super().async_setup(config):
            return False
        self.controller.register_view(IntentHandleView(self))

        await self.controller.setup.async_process_integration_platforms(
            self.domain, _async_process_intent_platform
        )

        intent_domain = self.controller.components.homeassistant.domain
        self.controller.intents.register_handler(
            _intent.ServiceHandler(
                _intent.INTENT_TURN_ON,
                intent_domain,
                _const.SERVICE_TURN_ON,
                "Turned {} on",
            ),
        )
        self.controller.intents.register_handler(
            _intent.ServiceHandler(
                _intent.INTENT_TURN_OFF,
                intent_domain,
                _const.SERVICE_TURN_OFF,
                "Turned {} off",
            ),
        )
        self.controller.intents.register_handler(
            _intent.ServiceHandler(
                _intent.INTENT_TOGGLE,
                intent_domain,
                _const.SERVICE_TOGGLE,
                "Toggled {}",
            ),
        )

        return True


async def _async_process_intent_platform(
    _domain: str, platform: core.PlatformImplementation
):
    """Process the intents of an integration."""
    if isinstance(platform, _intent.Platform):
        await platform.async_setup_intents()
