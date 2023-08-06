"""
My Smart Home Controller Component for Smart Home - The Next Generation.

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

_URL_PATH: typing.Final = "_my_redirect"


# pylint: disable=unused-variable
class MyComponent(core.SmartHomeControllerComponent):
    """Support for my.home-assistant.io redirect service."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Register hidden _my_redirect panel."""
        if not await super().async_setup(config):
            return False

        frontend = self.controller.components.frontend
        if not isinstance(frontend, core.FrontendComponent):
            return False

        frontend.async_register_built_in_panel(self.domain, frontend_url_path=_URL_PATH)
        return True
