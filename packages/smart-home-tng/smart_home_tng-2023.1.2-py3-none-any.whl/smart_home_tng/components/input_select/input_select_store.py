"""
Input Select Component for Smart Home - The Next Generation.

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
from .util import _remove_duplicates


# pylint: disable=unused-variable
class InputSelectStore(core.Store):
    """Store entity registry data."""

    async def _async_migrate_func(
        self,
        old_major_version: int,
        old_minor_version: int,
        old_data: dict[str, typing.Any],
    ) -> dict[str, typing.Any]:
        """Migrate to the new version."""
        if old_major_version == 1:
            if old_minor_version < 2:
                for item in old_data["items"]:
                    options = item[core.Select.ATTR_OPTIONS]
                    item[core.Select.ATTR_OPTIONS] = _remove_duplicates(
                        options, item.get(core.Const.CONF_NAME)
                    )
        return old_data
