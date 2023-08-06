"""
Scene Component for Smart Home - The Next Generation.

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

import logging
import typing

import voluptuous as vol

from ... import core


# pylint: disable=unused-variable
class SceneComponent(core.SmartHomeControllerComponent):
    """Allow users to set and activate scenes."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    async def async_setup(self, config: core.ConfigType) -> bool:
        if not await super().async_setup(config):
            return False

        component = core.EntityComponent(
            logging.getLogger(__name__), self.domain, self._shc
        )
        self._component = component

        await component.async_setup(config)

        # Ensure Smart Home TNG platform always loaded.
        await component.async_setup_platform(
            core.Const.CORE_COMPONENT_NAME,
            {"platform": core.Const.CORE_COMPONENT_NAME, core.Const.CONF_STATES: []},
        )

        # pylint: disable=protected-access
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON,
            {
                core.Const.ATTR_TRANSITION: vol.All(
                    vol.Coerce(float), vol.Clamp(min=0, max=6553)
                )
            },
            "_async_activate",
        )
        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        return await self._component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        return await self._component.async_unload_entry(entry)
