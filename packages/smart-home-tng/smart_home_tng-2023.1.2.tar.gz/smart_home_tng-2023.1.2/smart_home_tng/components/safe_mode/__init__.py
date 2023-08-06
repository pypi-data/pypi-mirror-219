"""
Recorder Component for Smart Home - The Next Generation.

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


class SafeModeComponent(core.SmartHomeControllerComponent):
    """The Safe Mode integration."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Safe Mode component."""
        persistent_notification: core.PersistentNotificationComponent = (
            self.controller.components.persistent_notification
        )
        if persistent_notification:
            persistent_notification.async_create(
                "Smart Home - The Next Generation is running in safe mode. "
                + "Check [the error log](/config/logs) to see what went wrong.",
                "Safe Mode",
            )
        return True


# pylint: disable=unused-variable

_: typing.Final = SafeModeComponent(__path__)
