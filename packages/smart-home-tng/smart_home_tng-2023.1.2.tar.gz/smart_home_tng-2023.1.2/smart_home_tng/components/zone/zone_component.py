"""
Zone Component for Smart Home - The Next Generation.

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

import logging
import typing
import voluptuous as vol

from ... import core
from .const import Const
from .zone import Zone
from .zone_storage_collection import ZoneStorageCollection

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)

_TRIGGER_SCHEMA = _cv.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_PLATFORM): "zone",
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_ids_or_uuids,
        vol.Required(core.Const.CONF_ZONE): _cv.entity_id,
        vol.Required(core.Const.CONF_EVENT, default=core.Zone.DEFAULT_EVENT): vol.Any(
            core.Zone.EVENT_ENTER, core.Zone.EVENT_LEAVE
        ),
    }
)


# pylint: disable=unused-variable
class ZoneComponent(core.ZoneComponent, core.TriggerPlatform):
    """Support for the definition of zones."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._storage_collection: ZoneStorageCollection = None
        self._yaml_collection: core.YamlCollection = None
        self._supported_platforms = frozenset([core.Platform.TRIGGER])

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                vol.Optional(self.domain, default=[]): vol.Any(
                    vol.All(_cv.ensure_list, [vol.Schema(Const.CREATE_FIELDS)]),
                    _empty_value,
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up configured zones as well as Home Assistant zone if necessary."""
        if not await super().async_setup(config):
            return False

        component = core.EntityComponent(_LOGGER, self.domain, self._shc)
        id_manager = core.IDManager()

        yaml_collection = core.IDLessCollection(
            logging.getLogger(f"{__name__}.yaml_collection"), id_manager
        )
        yaml_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, Zone.from_yaml
        )

        storage_collection = ZoneStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, Zone
        )

        self._component = component
        self._storage_collection = storage_collection
        self._yaml_collection = yaml_collection

        if config[self.domain]:
            await yaml_collection.async_load(config[self.domain])

        await storage_collection.async_load()

        core.StorageCollectionWebSocket(
            storage_collection,
            self.domain,
            self.domain,
            Const.CREATE_FIELDS,
            Const.UPDATE_FIELDS,
        ).async_setup()

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            core.Const.SERVICE_RELOAD,
            self._reload_service_handler,
            schema=Const.RELOAD_SERVICE_SCHEMA,
        )

        if not component.get_entity("zone.home"):
            home_zone = Zone(_home_conf(self._shc.config))
            # home_zone.entity_id = Const.ENTITY_ID_HOME
            await component.async_add_entities([home_zone])

        self._shc.bus.async_listen(
            core.Const.EVENT_CORE_CONFIG_UPDATE, self._core_config_updated
        )

        return True

    async def _core_config_updated(self, _: core.Event) -> None:
        """Handle core config updated."""
        home_zone = self._component.get_entity(Const.ENTITY_ID_HOME)
        if not home_zone:
            return
        await home_zone.async_update_config(_home_conf(self._shc.config, False))

    async def _reload_service_handler(self, _service_call: core.ServiceCall) -> None:
        """Remove all zones and load new ones from config."""
        conf = await self._component.async_prepare_reload(skip_reset=True)
        if conf is None:
            return
        await self._yaml_collection.async_load(conf[self.domain])

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up zone as config entry."""
        storage_collection = self._storage_collection

        data = dict(entry.data)
        data.setdefault(Const.CONF_PASSIVE, Const.DEFAULT_PASSIVE)
        data.setdefault(core.Const.CONF_RADIUS, Const.DEFAULT_RADIUS)

        await storage_collection.async_create_item(data)

        self._shc.async_create_task(
            self._shc.config_entries.async_remove(entry.entry_id)
        )

        return True

    async def async_unload_entry(self, _entry: core.ConfigEntry) -> bool:
        """Will be called once we remove it."""
        return True

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate trigger config."""
        config = _TRIGGER_SCHEMA(config)
        registry = self._shc.entity_registry
        config[core.Const.CONF_ENTITY_ID] = registry.async_validate_entity_ids(
            config[core.Const.CONF_ENTITY_ID]
        )
        return config

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for state changes based on configuration."""
        return await core.Zone.async_attach_trigger(
            self.controller, config, action, trigger_info
        )

    def get_zone_from_position(
        self, latitude: float, longitude: float, radius: int = 0
    ) -> core.State:
        """Find the active zone for given latitude, longitude.

        This method must be run in the event loop.
        """
        # Sort entity IDs so that we are deterministic if equal distance to 2 zones
        zones = (
            self._shc.states.get(entity_id)
            for entity_id in sorted(self._shc.states.async_entity_ids(self.domain))
        )

        min_dist = None
        closest: core.State = None

        for zone in zones:
            if zone.state == core.Const.STATE_UNAVAILABLE or zone.attributes.get(
                Const.ATTR_PASSIVE
            ):
                continue

            zone_dist = core.LocationInfo.distance(
                latitude,
                longitude,
                zone.attributes[core.Const.ATTR_LATITUDE],
                zone.attributes[core.Const.ATTR_LONGITUDE],
            )

            if zone_dist is None:
                continue

            within_zone = zone_dist - radius < zone.attributes[Const.ATTR_RADIUS]
            closer_zone = closest is None or zone_dist < min_dist
            smaller_zone = (
                zone_dist == min_dist
                and zone.attributes[Const.ATTR_RADIUS]
                < closest.attributes[Const.ATTR_RADIUS]
            )

            if within_zone and (closer_zone or smaller_zone):
                min_dist = zone_dist
                closest = zone

        return closest

    def in_zone(
        self, zone: core.State, latitude: float, longitude: float, radius: float = 0
    ) -> bool:
        """Test if given latitude, longitude is in given zone.

        Async friendly.
        """
        if zone.state == core.Const.STATE_UNAVAILABLE:
            return False

        zone_dist = core.LocationInfo.distance(
            latitude,
            longitude,
            zone.attributes[core.Const.ATTR_LATITUDE],
            zone.attributes[core.Const.ATTR_LONGITUDE],
        )

        if zone_dist is None or zone.attributes[Const.ATTR_RADIUS] is None:
            return False
        return zone_dist - radius < typing.cast(
            float, zone.attributes[Const.ATTR_RADIUS]
        )


def _empty_value(value: typing.Any) -> typing.Any:
    """Test if the user has the default config value from adding "zone:"."""
    if isinstance(value, dict) and len(value) == 0:
        return []

    raise vol.Invalid("Not a default value")


@core.callback
def _home_conf(config: core.Config, include_entity_id: bool = True) -> dict:
    """Return the home zone config."""
    result = {
        core.Const.CONF_NAME: config.location_name,
        core.Const.CONF_LATITUDE: config.latitude,
        core.Const.CONF_LONGITUDE: config.longitude,
        core.Const.CONF_RADIUS: Const.DEFAULT_RADIUS,
        core.Const.CONF_ICON: Const.ICON_HOME,
        Const.CONF_PASSIVE: False,
    }
    if include_entity_id:
        result[core.Const.CONF_ENTITY_ID] = Const.ENTITY_ID_HOME
    return result
