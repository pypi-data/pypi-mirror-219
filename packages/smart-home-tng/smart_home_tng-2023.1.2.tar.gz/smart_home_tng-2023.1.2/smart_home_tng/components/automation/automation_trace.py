"""
Automation Integration for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class AutomationTrace(core.ActionTrace):
    """Container for automation trace."""

    def __init__(
        self,
        domain: str,
        item_id: str,
        config: dict[str, typing.Any],
        blueprint_inputs: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Container for automation trace."""
        super().__init__(domain, item_id, config, blueprint_inputs, context)
        self._trigger_description: str = None

    def set_trigger_description(self, trigger: str) -> None:
        """Set trigger description."""
        self._trigger_description = trigger

    def as_short_dict(self) -> dict[str, typing.Any]:
        """Return a brief dictionary version of this AutomationTrace."""
        if self._short_dict:
            return self._short_dict

        result = super().as_short_dict()
        result["trigger"] = self._trigger_description
        return result
