"""
Blueprint Integration for Smart Home - The Next Generation.

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

import voluptuous as vol
import voluptuous.humanize as vh

from .blueprint_with_name_exception import BlueprintWithNameException


# pylint: disable=unused-variable
class InvalidBlueprint(BlueprintWithNameException):
    """When we encountered an invalid blueprint."""

    def __init__(
        self,
        domain: str,
        blueprint_name: str,
        blueprint_data: typing.Any,
        msg_or_exc: vol.Invalid,
    ) -> None:
        """Initialize an invalid blueprint error."""
        if isinstance(msg_or_exc, vol.Invalid):
            msg_or_exc = vh.humanize_error(blueprint_data, msg_or_exc)

        super().__init__(
            domain,
            blueprint_name,
            f"Invalid blueprint: {msg_or_exc}",
        )
        self.blueprint_data = blueprint_data
