"""
Homematic Integration for Smart Home - The Next Generation.

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

from ... import core
from .const import Const


# pylint: disable=unused-variable
class HomematicNotificationService(core.BaseNotificationService):
    """Implement the notification service for Homematic."""

    def __init__(self, owner: core.SmartHomeControllerComponent, data: dict):
        """Initialize the service."""
        super().__init__(owner.controller)
        self._data = data
        self._owner = owner

    def send_message(self, _message="", **kwargs):
        """Send a notification to the device."""
        data = {**self._data, **kwargs.get(core.Notify.ATTR_DATA, {})}

        if data.get(Const.ATTR_VALUE) is not None:
            templ = core.Template(self._data[Const.ATTR_VALUE], self._shc)
            data[Const.ATTR_VALUE] = templ.render_complex(templ, None)

        self._shc.services.call(
            self._owner.domain, Const.SERVICE_SET_DEVICE_VALUE, data
        )
