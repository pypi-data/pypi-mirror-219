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
class EditKeyBasedConfigView(BaseEditConfigView):
    """Configure a list of entries."""

    def _empty_config(self):
        """Return an empty config."""
        return {}

    def _get_value(self, _shc: core.SmartHomeController, data: dict, config_key: str):
        """Get value."""
        return data.get(config_key)

    def _write_value(
        self,
        _shc: core.SmartHomeController,
        data: dict,
        config_key: str,
        new_value: dict,
    ):
        """Set value."""
        data.setdefault(config_key, {}).update(new_value)

    def _delete_value(
        self, _shc: core.SmartHomeController, data: dict, config_key: str
    ):
        """Delete value."""
        return data.pop(config_key)
