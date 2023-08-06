"""
Core components of Smart Home - The Next Generation.

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

from .config_validation import ConfigValidation as cv
from .const import Const
from .service_call import ServiceCall


# pylint: disable=unused-variable
class ServiceTargetSelector:
    """Class to hold a target selector for a service."""

    def __init__(self, service_call: ServiceCall) -> None:
        """Extract ids from service call data."""
        entity_ids: str | list = service_call.data.get(Const.ATTR_ENTITY_ID)
        device_ids: str | list = service_call.data.get(Const.ATTR_DEVICE_ID)
        area_ids: str | list = service_call.data.get(Const.ATTR_AREA_ID)

        self._entity_ids = (
            set(cv.ensure_list(entity_ids)) if _has_match(entity_ids) else set()
        )
        self._device_ids = (
            set(cv.ensure_list(device_ids)) if _has_match(device_ids) else set()
        )
        self._area_ids = (
            set(cv.ensure_list(area_ids)) if _has_match(area_ids) else set()
        )

    @property
    def entity_ids(self) -> str | list:
        return self._entity_ids

    @property
    def device_ids(self) -> str | list:
        return self._device_ids

    @property
    def area_ids(self) -> str | list:
        return self._area_ids

    @property
    def has_any_selector(self) -> bool:
        """Determine if any selectors are present."""
        return bool(self._entity_ids or self._device_ids or self._area_ids)


def _has_match(ids: str | list[str]) -> typing.TypeGuard[str | list[str]]:
    """Check if ids can match anything."""
    return ids not in (None, Const.ENTITY_MATCH_NONE)
