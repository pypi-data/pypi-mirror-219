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

import abc
import asyncio
import collections
import collections.abc
import datetime
import logging
import math
import sys
import timeit
import typing

from . import helpers
from .callback import callback
from .callback_type import CallbackType
from .const import Const
from .context import Context
from .device_info import DeviceInfo
from .entity_category import EntityCategory
from .entity_description import EntityDescription
from .entity_platform_state import EntityPlatformState
from .entity_registry_entry import EntityRegistryEntry
from .event import Event
from .no_entity_specified_error import NoEntitySpecifiedError
from .smart_home_controller_error import SmartHomeControllerError
from .state_type import StateType
from .unit_conversion import TemperatureConverter

_SLOW_UPDATE_WARNING: typing.Final = 10
_DATA_ENTITY_SOURCE: typing.Final = "entity.info"
_DATA_CUSTOMIZE: typing.Final = "setup.shc_customize"
_SOURCE_CONFIG_ENTRY: typing.Final = "config_entry"
_SOURCE_PLATFORM_CONFIG: typing.Final = "platform_config"

# Used when converting float states to string: limit precision according to machine
# epsilon to make the string representation readable
_FLOAT_PRECISION: typing.Final = (
    abs(int(math.floor(math.log10(abs(sys.float_info.epsilon))))) - 1
)

_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class EntityPlatform:
        pass

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .entity_platform import EntityPlatform
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class Entity(abc.ABC):
    """An abstract class for Home Assistant entities."""

    # SAFE TO OVERWRITE
    # The properties and methods here are safe to overwrite when inheriting
    # this class. These may be used to customize the behavior of the entity.
    _entity_id: str = None

    # Owning SmartHomeController instance. Will be set by EntityPlatform
    # While not purely typed, it makes typehinting more useful for us
    # and removes the need for constant None checks or asserts.
    _shc: SmartHomeController = None

    # Owning platform instance. Will be set by EntityPlatform
    _platform: EntityPlatform = None

    # Entity description instance for this Entity
    _entity_description: EntityDescription

    # If we reported if this entity was slow
    _slow_reported = False

    # If we reported this entity is updated while disabled
    _disabled_reported = False

    # If we reported this entity is relying on deprecated temperature conversion
    _temperature_reported = False

    # Protect for multiple updates
    _update_staged = False

    # Process updates in parallel
    _parallel_updates: asyncio.Semaphore = None

    # Entry in the entity registry
    _registry_entry: EntityRegistryEntry = None

    # Hold list for functions to call on remove.
    _on_remove: list[CallbackType] = None

    # Context
    _context: Context = None
    _context_set: datetime.datetime = None

    # If entity is added to an entity platform
    _platform_state = EntityPlatformState.NOT_ADDED

    # Entity Properties
    _attr_assumed_state: bool = False
    _attr_attribution: str = None
    _attr_available: bool = True
    _attr_context_recent_time: datetime.timedelta = datetime.timedelta(seconds=5)
    _attr_device_class: str
    _attr_device_info: DeviceInfo = None
    _attr_entity_category: EntityCategory
    _attr_has_entity_name: bool
    _attr_entity_picture: str = None
    _attr_entity_registry_enabled_default: bool
    _attr_entity_registry_visible_default: bool
    _attr_extra_state_attributes: collections.abc.MutableMapping[str, typing.Any]
    _attr_force_update: bool
    _attr_icon: str
    _attr_name: str
    _attr_should_poll: bool = True
    _attr_state: StateType = Const.STATE_UNKNOWN
    _attr_supported_features: int = None
    _attr_unique_id: str = None
    _attr_unit_of_measurement: str = None

    @property
    def entity_id(self) -> str:
        if hasattr(self, "_entity_id"):
            return self._entity_id
        return None

    @property
    def platform(self) -> EntityPlatform:
        return self._platform

    @property
    def entity_description(self) -> EntityDescription:
        if hasattr(self, "_entity_description"):
            return self._entity_description
        return None

    @property
    def parallel_updates(self) -> asyncio.Semaphore:
        return self._parallel_updates

    @property
    def registry_entry(self) -> EntityRegistryEntry:
        return self._registry_entry

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return self._attr_should_poll

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._attr_unique_id

    @property
    def has_entity_name(self) -> bool:
        """Return if the name of the entity is describing only the entity itself."""
        if hasattr(self, "_attr_has_entity_name"):
            return self._attr_has_entity_name
        if hasattr(self, "_entity_description"):
            return self.entity_description.has_entity_name
        return False

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        if hasattr(self, "_attr_name"):
            return self._attr_name
        if hasattr(self, "_entity_description"):
            return self.entity_description.name
        return None

    @property
    def state(self) -> StateType:
        """Return the state of the entity."""
        return self._attr_state

    @property
    def capability_attributes(self) -> collections.abc.Mapping[str, typing.Any]:
        """Return the capability attributes.

        Attributes that explain the capabilities of an entity.

        Implemented by component base class. Convention for attribute names
        is lowercase snake_case.
        """
        return None

    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the state attributes.

        Implemented by component base class, should not be extended by integrations.
        Convention for attribute names is lowercase snake_case.
        """
        return None

    @property
    def device_state_attributes(self) -> collections.abc.Mapping[str, typing.Any]:
        """Return entity specific state attributes.

        This method is deprecated, platform classes should implement
        extra_state_attributes instead.
        """
        return None

    @property
    def extra_state_attributes(self) -> collections.abc.Mapping[str, typing.Any]:
        """Return entity specific state attributes.

        Implemented by platform classes. Convention for attribute names
        is lowercase snake_case.
        """
        if hasattr(self, "_attr_extra_state_attributes"):
            return self._attr_extra_state_attributes
        return None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device specific attributes.

        Implemented by platform classes.
        """
        return self._attr_device_info

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if hasattr(self, "_entity_description"):
            return str(self.entity_description.device_class)
        return None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        if hasattr(self, "_attr_unit_of_measurement"):
            return self._attr_unit_of_measurement
        if hasattr(self, "_entity_description"):
            return self.entity_description.unit_of_measurement
        return None

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        if hasattr(self, "_attr_icon"):
            return self._attr_icon
        if hasattr(self, "_entity_description"):
            return self.entity_description.icon
        return None

    @property
    def entity_picture(self) -> str:
        """Return the entity picture to use in the frontend, if any."""
        return self._attr_entity_picture

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._attr_available

    @property
    def assumed_state(self) -> bool:
        """Return True if unable to access real state of the entity."""
        return self._attr_assumed_state

    @property
    def force_update(self) -> bool:
        """Return True if state updates should be forced.

        If True, a state change will be triggered anytime the state property is
        updated, not just when the value changes.
        """
        if hasattr(self, "_attr_force_update"):
            return self._attr_force_update
        if hasattr(self, "_entity_description"):
            return self.entity_description.force_update
        return False

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._attr_supported_features

    @property
    def context_recent_time(self) -> datetime.timedelta:
        """Time that a context is considered recent."""
        return self._attr_context_recent_time

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        if hasattr(self, "_attr_entity_registry_enabled_default"):
            return self._attr_entity_registry_enabled_default
        if hasattr(self, "_entity_description"):
            return self.entity_description.entity_registry_enabled_default
        return True

    @property
    def entity_registry_visible_default(self) -> bool:
        """Return if the entity should be visible when first added to the entity registry."""
        if hasattr(self, "_attr_entity_registry_visible_default"):
            return self._attr_entity_registry_visible_default
        if hasattr(self, "_entity_description"):
            return self.entity_description.entity_registry_visible_default
        return True

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return self._attr_attribution

    @property
    def entity_category(self) -> EntityCategory:
        """Return the category of the entity, if any."""
        if hasattr(self, "_attr_entity_category"):
            return self._attr_entity_category
        if hasattr(self, "_entity_description"):
            return self.entity_description.entity_category
        return None

    # DO NOT OVERWRITE
    # These properties and methods are either managed by Home Assistant or they
    # are used to perform a very specific function. Overwriting these may
    # produce undesirable effects in the entity's operation.

    @property
    def enabled(self) -> bool:
        """Return if the entity is enabled in the entity registry.

        If an entity is not part of the registry, it cannot be disabled
        and will therefore always be enabled.
        """
        return self._registry_entry is None or not self._registry_entry.disabled

    @callback
    def async_set_context(self, context: Context) -> None:
        """Set the context the entity currently operates under."""
        self._context = context
        self._context_set = helpers.utcnow()

    async def async_update_state(self, force_refresh: bool = False) -> None:
        """Update Home Assistant with current state of entity.

        If force_refresh == True will update entity before setting state.

        This method must be run in the event loop.
        """
        if self._shc is None:
            raise RuntimeError(f"Attribute shc is None for {self}")

        if self._entity_id is None:
            raise NoEntitySpecifiedError(
                f"No entity id specified for entity {self.name}"
            )

        # update entity data
        if force_refresh:
            try:
                await self.async_device_update()
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Update for {self._entity_id} fails")
                return

        self._async_write_state()

    @callback
    def async_write_state(self) -> None:
        """Write the state to the state machine."""
        if self._shc is None:
            raise RuntimeError(f"Attribute hass is None for {self}")

        if self._entity_id is None:
            raise NoEntitySpecifiedError(
                f"No entity id specified for entity {self.name}"
            )

        self._async_write_state()

    def _stringify_state(self, available: bool) -> str:
        """Convert state to string."""
        if not available:
            return Const.STATE_UNAVAILABLE
        if (state := self.state) is None:
            return Const.STATE_UNKNOWN
        if isinstance(state, float):
            # If the entity's state is a float, limit precision according to machine
            # epsilon to make the string representation readable
            return f"{state:.{_FLOAT_PRECISION}}"
        return str(state)

    @callback
    def _async_write_state(self) -> None:
        """Write the state to the state machine."""
        if self._platform_state == EntityPlatformState.REMOVED:
            # Polling returned after the entity has already been removed
            return

        if self._registry_entry and self._registry_entry.disabled_by:
            if not self._disabled_reported:
                self._disabled_reported = True
                assert self.platform is not None
                _LOGGER.warning(
                    f"Entity {self._entity_id} is incorrectly being triggered for "
                    + "updates while it is disabled. This is a bug in the "
                    + f"{self._platform.platform_name} integration"
                )
            return

        start = timeit.default_timer()

        attr = self.capability_attributes
        attr = dict(attr) if attr else {}

        available = self.available  # only call self.available once per update cycle
        state = self._stringify_state(available)
        if available:
            attr.update(self.state_attributes or {})
            attr.update(self.extra_state_attributes or {})

        if (unit_of_measurement := self.unit_of_measurement) is not None:
            attr[Const.ATTR_UNIT_OF_MEASUREMENT] = unit_of_measurement

        entry = self.registry_entry

        if assumed_state := self.assumed_state:
            attr[Const.ATTR_ASSUMED_STATE] = assumed_state

        if (attribution := self.attribution) is not None:
            attr[Const.ATTR_ATTRIBUTION] = attribution

        if (
            device_class := (entry and entry.device_class) or self.device_class
        ) is not None:
            attr[Const.ATTR_DEVICE_CLASS] = str(device_class)

        if (entity_picture := self.entity_picture) is not None:
            attr[Const.ATTR_ENTITY_PICTURE] = entity_picture

        if (icon := (entry and entry.icon) or self.icon) is not None:
            attr[Const.ATTR_ICON] = icon

        def friendly_name() -> str | None:
            """Return the friendly name.

            If has_entity_name is False, this returns self.name
            If has_entity_name is True, this returns device.name + self.name
            """
            if not self.has_entity_name or not self.registry_entry:
                return self.name

            device_registry = self._shc.device_registry
            if not (device_id := self.registry_entry.device_id) or not (
                device_entry := device_registry.async_get(device_id)
            ):
                return self.name

            if not self.name:
                return device_entry.name_by_user or device_entry.name
            return f"{device_entry.name_by_user or device_entry.name} {self.name}"

        if (name := (entry and entry.name) or friendly_name()) is not None:
            attr[Const.ATTR_FRIENDLY_NAME] = name

        if (supported_features := self.supported_features) is not None:
            attr[Const.ATTR_SUPPORTED_FEATURES] = supported_features

        end = timeit.default_timer()

        if end - start > 0.4 and not self._slow_reported:
            self._slow_reported = True
            report_issue = self._suggest_report_issue()
            _LOGGER.warning(
                f"Updating state for {self._entity_id} ({type(self)}) took "
                + f"{end- start:.3f} seconds. Please {report_issue}"
            )

        # Overwrite properties that have been set in the config file.
        if _DATA_CUSTOMIZE in self._shc.data:
            attr.update(self._shc.data[_DATA_CUSTOMIZE].get(self._entity_id))

        def _convert_temperature(state: str, attr: dict[str, typing.Any]) -> str:
            unit_of_measure = attr.get(Const.ATTR_UNIT_OF_MEASUREMENT)
            if unit_of_measure is None:
                return state

            units = self._shc.config.units
            if (
                unit_of_measure == units.temperature_unit
                or unit_of_measure not in TemperatureConverter.VALID_UNITS
            ):
                return state

            domain = helpers.split_entity_id(self.entity_id)[0]
            if domain != "sensor":
                if not self._temperature_reported:
                    self._temperature_reported = True
                    report_issue = self._suggest_report_issue()
                    _LOGGER.warning(
                        f"Entity {self._entity_id} ({type(self)}) relies on automatic "
                        + "temperature conversion, this will be unsupported in "
                        + f"Home Assistant Core 2022.7. Please {report_issue}"
                    )
            elif not isinstance(self, _SensorEntityBase):
                if not self._temperature_reported:
                    self._temperature_reported = True
                    report_issue = self._suggest_report_issue()
                    _LOGGER.warning(
                        f"Temperature sensor {self._entity_id} ({type(self)}) does not "
                        + "inherit SensorEntity, "
                        + "this will be unsupported in Home Assistant Core 2022.7."
                        + f"Please {report_issue}"
                    )
            else:
                return state

            try:
                prec = len(state) - state.index(".") - 1 if "." in state else 0
                temp = units.temperature(float(state), unit_of_measure)
                state = str(round(temp) if prec == 0 else round(temp, prec))
                attr[Const.ATTR_UNIT_OF_MEASUREMENT] = units.temperature_unit
            except ValueError:
                # Could not convert state to float
                pass
            return state

        state = _convert_temperature(state, attr)

        if (
            self._context_set is not None
            and helpers.utcnow() - self._context_set > self.context_recent_time
        ):
            self._context = None
            self._context_set = None

        self._shc.states.async_set(
            self._entity_id, state, attr, self.force_update, self._context
        )

    def schedule_update_state(self, force_refresh: bool = False) -> None:
        """Schedule an update ha state change task.

        Scheduling the update avoids executor deadlocks.

        Entity state and attributes are read when the update ha state change
        task is executed.
        If state is changed more than once before the ha state change task has
        been executed, the intermediate state transitions will be missed.
        """
        self._shc.add_job(self.async_update_state(force_refresh))

    @callback
    def async_schedule_update_state(self, force_refresh: bool = False) -> None:
        """Schedule an update ha state change task.

        This method must be run in the event loop.
        Scheduling the update avoids executor deadlocks.

        Entity state and attributes are read when the update ha state change
        task is executed.
        If state is changed more than once before the ha state change task has
        been executed, the intermediate state transitions will be missed.
        """
        if force_refresh:
            self._shc.async_create_task(self.async_update_state(force_refresh))
        else:
            self.async_write_state()

    async def async_device_update(self, warning: bool = True) -> None:
        """Process 'update' or 'async_update' from entity.

        This method is a coroutine.
        """
        if self._update_staged:
            return
        self._update_staged = True

        # Process update sequential
        if self.parallel_updates:
            await self.parallel_updates.acquire()

        try:
            task: asyncio.Future[None]
            if hasattr(self, "async_update"):
                task = self._shc.async_create_task(self.async_update())
            elif hasattr(self, "update"):
                task = self._shc.async_add_executor_job(self.update)
            else:
                return

            if not warning:
                await task
                return

            finished, _ = await asyncio.wait([task], timeout=_SLOW_UPDATE_WARNING)

            for done in finished:
                if exc := done.exception():
                    raise exc
                return

            _LOGGER.warning(
                f"Update of {self._entity_id} is taking over {_SLOW_UPDATE_WARNING} seconds",
            )
            await task
        finally:
            self._update_staged = False
            if self.parallel_updates:
                self.parallel_updates.release()

    @callback
    def async_on_remove(self, func: CallbackType) -> None:
        """Add a function to call when entity is removed or not added."""
        if self._on_remove is None:
            self._on_remove = []
        self._on_remove.append(func)

    async def async_removed_from_registry(self) -> None:
        """Run when entity has been removed from entity registry.

        To be extended by integrations.
        """

    @callback
    def add_to_platform_start(
        self,
        shc: SmartHomeController,
        platform: EntityPlatform,
        parallel_updates: asyncio.Semaphore,
    ) -> None:
        """Start adding an entity to a platform."""
        if self._platform_state == EntityPlatformState.ADDED:
            raise SmartHomeControllerError(
                f"Entity {self.entity_id} cannot be added a second time to an entity platform"
            )

        self._shc = shc
        self._platform = platform
        self._parallel_updates = parallel_updates
        self._platform_state = EntityPlatformState.ADDED

    def _call_on_remove_callbacks(self) -> None:
        """Call callbacks registered by async_on_remove."""
        if self._on_remove is None:
            return
        while self._on_remove:
            self._on_remove.pop()()

    @callback
    def add_to_platform_abort(self) -> None:
        """Abort adding an entity to a platform."""

        self._platform_state = EntityPlatformState.NOT_ADDED
        self._call_on_remove_callbacks()

        self._shc = None
        self._platform = None
        self._parallel_updates = None

    async def add_to_platform_finish(self) -> None:
        """Finish adding an entity to a platform."""
        await self.async_internal_added_to_shc()
        await self.async_added_to_shc()
        self.async_write_state()

    async def async_remove(self, *, force_remove: bool = False) -> None:
        """Remove entity from Home Assistant.

        If the entity has a non disabled entry in the entity registry,
        the entity's state will be set to unavailable, in the same way
        as when the entity registry is loaded.

        If the entity doesn't have a non disabled entry in the entity registry,
        or if force_remove=True, its state will be removed.
        """
        if self.platform and self._platform_state != EntityPlatformState.ADDED:
            raise SmartHomeControllerError(
                f"Entity {self.entity_id} async_remove called twice"
            )

        self._platform_state = EntityPlatformState.REMOVED

        self._call_on_remove_callbacks()

        await self.async_internal_will_remove_from_shc()
        await self.async_will_remove_from_shc()

        # Check if entry still exists in entity registry (e.g. unloading config entry)
        if (
            not force_remove
            and self.registry_entry
            and not self.registry_entry.disabled
        ):
            # Set the entity's state will to unavailable + ATTR_RESTORED: True
            self.registry_entry.write_unavailable_state(self._shc)
        else:
            self._shc.states.async_remove(self.entity_id, context=self._context)

    async def async_added_to_shc(self) -> None:
        """Run when entity about to be added to the Smart Home Controller.

        To be extended by integrations.
        """

    async def async_will_remove_from_shc(self) -> None:
        """Run when entity will be removed from the Smart Home Controller.

        To be extended by integrations.
        """

    @callback
    def async_registry_entry_updated(self) -> None:
        """Run when the entity registry entry has been updated.

        To be extended by integrations.
        """

    async def async_internal_added_to_shc(self) -> None:
        """Run when entity about to be added to the Smart Home Controller.

        Not to be extended by integrations.
        """
        if self.platform:
            info = {
                "domain": self.platform.platform_name,
                "custom_component": "custom_components" in type(self).__module__,
            }

            if self.platform.config_entry:
                info["source"] = _SOURCE_CONFIG_ENTRY
                info["config_entry"] = self.platform.config_entry.entry_id
            else:
                info["source"] = _SOURCE_PLATFORM_CONFIG

            self._shc.data.setdefault(_DATA_ENTITY_SOURCE, {})[self.entity_id] = info

        if self.registry_entry is not None:
            # This is an assert as it should never happen, but helps in tests
            assert (
                not self.registry_entry.disabled_by
            ), f"Entity {self._entity_id} is being added while it's disabled"

            self.async_on_remove(
                self._shc.tracker.async_track_entity_registry_updated_event(
                    self.entity_id, self._async_registry_updated
                )
            )

    async def async_internal_will_remove_from_shc(self) -> None:
        """Run when entity will be removed from Smart Home Controller.

        Not to be extended by integrations.
        """
        if self.platform:
            self._shc.data[_DATA_ENTITY_SOURCE].pop(self.entity_id)

    async def _async_registry_updated(self, event: Event) -> None:
        """Handle entity registry update."""
        data = event.data
        if data["action"] == "remove":
            await self.async_removed_from_registry()
            self._registry_entry = None
            await self.async_remove()

        if data["action"] != "update":
            return

        ent_reg = self._shc.entity_registry
        old = self.registry_entry
        self._registry_entry = ent_reg.async_get(data["entity_id"])
        assert self.registry_entry is not None

        if self.registry_entry.disabled:
            await self.async_remove()
            return

        assert old is not None
        if self.registry_entry.entity_id == old.entity_id:
            self.async_registry_entry_updated()
            self.async_write_state()
            return

        await self.async_remove(force_remove=True)

        assert self.platform is not None
        self._entity_id = self.registry_entry.entity_id
        await self.platform.async_add_entities([self])

    def __eq__(self, other: typing.Any) -> bool:
        """Return the comparison."""
        if not isinstance(other, self.__class__):
            return False

        # Can only decide equality if both have a unique id
        if self.unique_id is None or other.unique_id is None:
            return False

        # Ensure they belong to the same platform
        if self.platform is not None or other.platform is not None:
            if self.platform is None or other.platform is None:
                return False

            if self.platform.platform != other.platform.platform:
                return False

        return self.unique_id == other.unique_id

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<Entity {self.name}: {self.state}>"

    async def async_request_call(
        self, coro: collections.abc.Coroutine[typing.Any, typing.Any, typing.Any]
    ) -> None:
        """Process request batched."""
        if self.parallel_updates:
            await self.parallel_updates.acquire()

        try:
            await coro
        finally:
            if self.parallel_updates:
                self.parallel_updates.release()

    def _suggest_report_issue(self) -> str:
        """Suggest to report an issue."""
        report_issue = ""
        if "custom_components" in type(self).__module__:
            report_issue = "report it to the custom component author."
        else:
            report_issue = (
                "create a bug report at "
                + "https://github.com/home-assistant/core/issues?q=is%3Aopen+is%3Aissue"
            )
            if self.platform:
                report_issue += (
                    f"+label%3A%22integration%3A+{self.platform.platform_name}%22"
                )

        return report_issue


class _SensorEntityBase(Entity):
    """
    Required base class for SensorEntity to avoid circular imports.

    Required for 'isinstance' test for wrong inheritance of sensor entities.
    """
