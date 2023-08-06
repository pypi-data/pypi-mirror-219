"""
Configuration API for Smart Home - The Next Generation.

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
from .base_edit_config_view import BaseEditConfigView


# pylint: disable=unused-variable
class EditIdBasedConfigView(BaseEditConfigView):
    """Configure key based config entries."""

    def _empty_config(self):
        """Return an empty config."""
        return []

    def _get_value(
        self, shc: core.SmartHomeController, data: core.JsonType, config_key: str
    ):
        """Get value."""
        return next(
            (val for val in data if val.get(core.Const.CONF_ID) == config_key), None
        )

    def _write_value(
        self,
        shc: core.SmartHomeController,
        data: core.JsonType,
        config_key: str,
        new_value: core.JsonType,
    ):
        """Set value."""
        if (value := self._get_value(shc, data, config_key)) is None:
            value = {core.Const.CONF_ID: config_key}
            data.append(value)

        value.update(new_value)

    def _delete_value(
        self, shc: core.SmartHomeController, data: core.JsonType, config_key: str
    ):
        """Delete value."""
        index = next(
            idx
            for idx, val in enumerate(data)
            if val.get(core.Const.CONF_ID) == config_key
        )
        data.pop(index)
