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

import collections
import collections.abc
import typing

import attr

from .area import Area
from .callback import callback
from .const import Const
from .store import Store


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_STORAGE_KEY: typing.Final = "core.area_registry"
_STORAGE_VERSION: typing.Final = 1
_SAVE_DELAY: typing.Final = 10
_UNDEFINED: typing.Final = object()


# pylint: disable=unused-variable
class AreaRegistry:
    """Class to hold a registry of areas."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the area registry."""
        self._shc = shc
        self._loaded = False
        self._areas: collections.abc.MutableMapping[str, Area] = {}
        self._store = Store[dict[str, list[dict[str, typing.Optional[str]]]]](
            shc, _STORAGE_VERSION, _STORAGE_KEY, atomic_writes=True
        )
        self._normalized_name_area_idx: dict[str, str] = {}

    @property
    def areas(self) -> collections.abc.MutableMapping[str, Area]:
        return self._areas

    @callback
    def async_get_area(self, area_id: str) -> Area:
        """Get area by id."""
        return self.areas.get(area_id)

    @callback
    def async_get_area_by_name(self, name: str) -> Area:
        """Get area by name."""
        normalized_name = self.normalize_area_name(name)
        if normalized_name not in self._normalized_name_area_idx:
            return None
        return self.areas[self._normalized_name_area_idx[normalized_name]]

    @callback
    def async_list_areas(self) -> collections.abc.Iterable[Area]:
        """Get all areas."""
        return self._areas.values()

    @callback
    def async_get_or_create(self, name: str) -> Area:
        """Get or create an area."""
        if area := self.async_get_area_by_name(name):
            return area
        return self.async_create(name)

    @callback
    def async_create(self, name: str, picture: str = None) -> Area:
        """Create a new area."""
        normalized_name = self.normalize_area_name(name)

        if self.async_get_area_by_name(name):
            raise ValueError(f"The name {name} ({normalized_name}) is already in use")

        area = Area(name=name, normalized_name=normalized_name, picture=picture)
        area.generate_id(self.areas)
        assert area.id is not None
        self._areas[area.id] = area
        self._normalized_name_area_idx[normalized_name] = area.id
        self.async_schedule_save()
        self._shc.bus.async_fire(
            Const.EVENT_AREA_REGISTRY_UPDATED, {"action": "create", "area_id": area.id}
        )
        return area

    @callback
    def async_delete(self, area_id: str) -> None:
        """Delete area."""
        area = self._areas[area_id]
        device_registry = self._shc.device_registry
        entity_registry = self._shc.entity_registry
        device_registry.async_clear_area_id(area_id)
        entity_registry.async_clear_area_id(area_id)

        del self.areas[area_id]
        del self._normalized_name_area_idx[area.normalized_name]

        self._shc.bus.async_fire(
            Const.EVENT_AREA_REGISTRY_UPDATED, {"action": "remove", "area_id": area_id}
        )

        self.async_schedule_save()

    @callback
    def async_update(
        self,
        area_id: str,
        name: str | object = _UNDEFINED,
        picture: str | object = _UNDEFINED,
    ) -> Area:
        """Update name of area."""
        updated = self._async_update(area_id, name=name, picture=picture)
        self._shc.bus.async_fire(
            Const.EVENT_AREA_REGISTRY_UPDATED, {"action": "update", "area_id": area_id}
        )
        return updated

    @callback
    def _async_update(
        self,
        area_id: str,
        name: str | object = _UNDEFINED,
        picture: str | object = _UNDEFINED,
    ) -> Area:
        """Update name of area."""
        old = self.areas[area_id]

        changes = {}

        if picture is not _UNDEFINED:
            changes["picture"] = picture

        normalized_name = None

        if name is not _UNDEFINED and name != old.name:
            normalized_name = self.normalize_area_name(name)

            if normalized_name != old.normalized_name and self.async_get_area_by_name(
                name
            ):
                raise ValueError(
                    f"The name {name} ({normalized_name}) is already in use"
                )

            changes["name"] = name
            changes["normalized_name"] = normalized_name

        if not changes:
            return old

        new = self.areas[area_id] = attr.evolve(old, **changes)
        if normalized_name is not None:
            self._normalized_name_area_idx[
                normalized_name
            ] = self._normalized_name_area_idx.pop(old.normalized_name)

        self.async_schedule_save()
        return new

    async def async_load(self) -> None:
        """Load the area registry."""
        if self._loaded:
            return None
        self._loaded = True
        data = await self._store.async_load()

        areas: collections.abc.MutableMapping[str, Area] = collections.OrderedDict()

        if isinstance(data, dict):
            for area in data["areas"]:
                normalized_name = self.normalize_area_name(area["name"])
                areas[area["id"]] = Area(
                    name=area["name"],
                    id=area["id"],
                    # New in 2021.11
                    picture=area.get("picture"),
                    normalized_name=normalized_name,
                )
                self._normalized_name_area_idx[normalized_name] = area["id"]

        self._areas = areas

    @callback
    def async_schedule_save(self) -> None:
        """Schedule saving the area registry."""
        self._store.async_delay_save(self._data_to_save, _SAVE_DELAY)

    @callback
    def _data_to_save(self) -> dict[str, list[dict[str, str]]]:
        """Return data of area registry to store in a file."""
        data = {}

        data["areas"] = [
            {"name": entry.name, "id": entry.id, "picture": entry.picture}
            for entry in self.areas.values()
        ]

        return data

    @staticmethod
    def normalize_area_name(area_name: str) -> str:
        """Normalize an area name by removing whitespace and case folding."""
        return area_name.casefold().replace(" ", "")
