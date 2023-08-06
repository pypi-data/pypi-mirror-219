"""
Dashboards Component for Smart Home - The Next Generation.

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

import asyncio
import logging
import typing

import voluptuous as vol

from ... import core
from .config_not_found import ConfigNotFound
from .const import Const
from .dashboards_collection import DashboardsCollection
from .lovelace_config import LovelaceConfig
from .lovelace_storage import LovelaceStorage
from .lovelace_yaml import LovelaceYAML
from .resource_storage_collection import ResourceStorageCollection
from .resource_yaml_collection import ResourceYAMLCollection

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)

_CONF_DASHBOARDS: typing.Final = "dashboards"

_YAML_DASHBOARD_SCHEMA: typing.Final = vol.Schema(
    {
        **Const.DASHBOARD_BASE_CREATE_FIELDS,
        vol.Required(core.Const.CONF_MODE): Const.MODE_YAML,
        vol.Required(core.Const.CONF_FILENAME): _cv.path,
    }
)

_LOVELACE_CONFIG: typing.Final = {
    "type": "lovelace/config",
    vol.Optional("force", default=False): bool,
    vol.Optional(Const.CONF_URL_PATH): vol.Any(None, _cv.string),
}

_LOVELACE_SAVE_CONFIG: typing.Final = {
    "type": "lovelace/config/save",
    "config": vol.Any(str, dict),
    vol.Optional(Const.CONF_URL_PATH): vol.Any(None, _cv.string),
}

_LOVELACE_DELETE_CONFIG: typing.Final = {
    "type": "lovelace/config/delete",
    vol.Optional(Const.CONF_URL_PATH): vol.Any(None, _cv.string),
}

_LOVELACE_RESOURCES: typing.Final = {"type": "lovelace/resources"}
_LOVELACE_DASHBOARDS: typing.Final = {"type": "lovelace/dashboards/list"}


# pylint: disable=unused-variable
class Dashboards(core.SmartHomeControllerComponent, core.SystemHealthPlatform):
    """Support for the Lovelace UI."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._mode: str = None
        self._dashboards: dict[str, LovelaceConfig] = {}
        self._yaml_dashboards: dict[str, core.ConfigType] = {}
        self._resource_collection = None
        self._frontend: core.FrontendComponent = None
        self._supported_platforms = frozenset([core.Platform.SYSTEM_HEALTH])

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                vol.Optional(self.domain, default={}): vol.Schema(
                    {
                        vol.Optional(
                            core.Const.CONF_MODE, default=Const.MODE_STORAGE
                        ): vol.All(
                            vol.Lower, vol.In([Const.MODE_YAML, Const.MODE_STORAGE])
                        ),
                        vol.Optional(_CONF_DASHBOARDS): _cv.schema_with_slug_keys(
                            _YAML_DASHBOARD_SCHEMA,
                            slug_validator=_url_slug,
                        ),
                        vol.Optional(core.Const.CONF_RESOURCES): [
                            Const.RESOURCE_SCHEMA
                        ],
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def _frontend_loaded(self, _shc: core.SmartHomeController, component: str):
        frontend = self.get_component(component)
        if isinstance(frontend, core.FrontendComponent):
            self._frontend = frontend
            frontend.async_register_built_in_panel(
                self.domain, config={"mode": self._mode}
            )

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Lovelace commands."""
        if not await super().async_setup(config):
            return False

        conf: core.ConfigType = config[self.domain]
        mode = conf[core.Const.CONF_MODE]
        yaml_resources = conf.get(core.Const.CONF_RESOURCES)

        shc = self._shc

        frontend = self.controller.components.frontend
        if isinstance(frontend, core.FrontendComponent):
            frontend.async_register_built_in_panel(self.domain, config={"mode": mode})
            self._frontend = frontend
        else:
            self._shc.setup.async_when_setup_or_start("frontend", self._frontend_loaded)

        if mode == Const.MODE_YAML:
            default_config = LovelaceYAML(shc, None, None)
            resource_collection = await _create_yaml_resource_col(shc, yaml_resources)

            core.Service.async_register_admin_service(
                shc,
                self.domain,
                Const.SERVICE_RELOAD_RESOURCES,
                self._reload_resources_service_handler,
                schema=Const.RESOURCE_RELOAD_SERVICE_SCHEMA,
            )

        else:
            default_config = LovelaceStorage(
                shc, None, self.storage_key, self.storage_version
            )

            if yaml_resources is not None:
                _LOGGER.warning(
                    "Lovelace is running in storage mode. Define resources via user interface"
                )

            resource_collection = ResourceStorageCollection(
                shc,
                default_config,
                f"{self.domain}.resources",
                Const.RESOURCES_STORAGE_VERSION,
            )

            core.StorageCollectionWebSocket(
                resource_collection,
                "lovelace/resources",
                "resource",
                Const.RESOURCE_CREATE_FIELDS,
                Const.RESOURCE_UPDATE_FIELDS,
            ).async_setup(create_list=False)

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        websocket_api.register_command(self._lovelace_config, _LOVELACE_CONFIG)
        websocket_api.register_command(
            self._lovelace_save_config, _LOVELACE_SAVE_CONFIG
        )
        websocket_api.register_command(
            self._lovelace_delete_config, _LOVELACE_DELETE_CONFIG
        )
        websocket_api.register_command(self._lovelace_resources, _LOVELACE_RESOURCES)

        websocket_api.register_command(self._lovelace_dashboards, _LOVELACE_DASHBOARDS)

        self._mode = mode
        self._resource_collection = resource_collection
        self._yaml_dashboards = conf.get(_CONF_DASHBOARDS, {})

        # We store a dictionary mapping url_path: config. None is the default.
        self._dashboards[None] = default_config

        if shc.config.safe_mode:
            return True

        # Process YAML dashboards
        for url_path, dashboard_conf in self._yaml_dashboards.items():
            # For now always mode=yaml
            config = LovelaceYAML(shc, url_path, dashboard_conf)
            self._dashboards[url_path] = config

            try:
                self._register_panel(url_path, Const.MODE_YAML, dashboard_conf, False)
            except ValueError:
                _LOGGER.warning(f"Panel url path {url_path} is not unique")

        # Process storage dashboards
        dashboards_collection = DashboardsCollection(
            shc, f"{self.domain}.dashboards", Const.DASHBOARDS_STORAGE_VERSION
        )

        dashboards_collection.async_add_listener(self._storage_dashboard_changed)
        await dashboards_collection.async_load()

        core.StorageCollectionWebSocket(
            dashboards_collection,
            "lovelace/dashboards",
            "dashboard",
            Const.STORAGE_DASHBOARD_CREATE_FIELDS,
            Const.STORAGE_DASHBOARD_UPDATE_FIELDS,
        ).async_setup(create_list=False)

        return True

    async def _storage_dashboard_changed(
        self, change_type: str, _item_id, item: core.ConfigType
    ):
        """Handle a storage dashboard change."""
        url_path = item[Const.CONF_URL_PATH]

        if change_type == core.Const.EVENT_COLLECTION_CHANGE_REMOVED:
            self._frontend.async_remove_panel(url_path)
            await self._dashboards.pop(url_path).async_delete()
            return

        if change_type == core.Const.EVENT_COLLECTION_CHANGE_ADDED:
            existing = self._dashboards.get(url_path)

            if existing:
                _LOGGER.warning(
                    f"Cannot register panel at {url_path}, "
                    + f"it is already defined in {existing}",
                )
                return

            self._dashboards[url_path] = LovelaceStorage(
                self._shc, item, self.storage_key, self.storage_version
            )

            update = False
        else:
            self._dashboards[url_path].config = item
            update = True

        try:
            self._register_panel(url_path, Const.MODE_STORAGE, item, update)
        except ValueError:
            _LOGGER.warning(f"Failed to {change_type} panel {url_path} from storage")

    async def _reload_resources_service_handler(
        self, _service_call: core.ServiceCall
    ) -> None:
        """Reload yaml resources."""
        try:
            conf = await self._shc.setup.async_shc_config_yaml()
        except core.SmartHomeControllerError as err:
            _LOGGER.error(err)
            return

        integration = await self._shc.setup.async_get_integration(self.domain)

        config = await self._shc.setup.async_process_component_config(conf, integration)

        resource_collection = await _create_yaml_resource_col(
            self._shc, config[self.domain].get(core.Const.CONF_RESOURCES)
        )
        self._resource_collection = resource_collection

    async def _lovelace_resources(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Send Lovelace UI resources over WebSocket configuration."""
        resources = self._resource_collection

        if not resources.loaded:
            await resources.async_load()

        connection.send_result(msg["id"], resources.async_items())

    async def _send_with_error_handling(
        self,
        func: typing.Callable[
            [core.WebSocket.Connection, dict, LovelaceConfig],
            typing.Awaitable[typing.Any],
        ],
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        url_path = msg.get(Const.CONF_URL_PATH)
        config = self._dashboards.get(url_path)

        if config is None:
            connection.send_error(
                msg["id"],
                "config_not_found",
                f"Unknown config specified: {url_path}",
            )
            return

        error = None
        try:
            result = await func(connection, msg, config)
        except ConfigNotFound:
            error = "config_not_found", "No config found."
        except core.SmartHomeControllerError as err:
            error = "error", str(err)

        if error is not None:
            connection.send_error(msg["id"], *error)
            return

        if msg is not None:
            await connection.send_big_result(msg["id"], result)
        else:
            connection.send_result(msg["id"], result)

    async def _lovelace_config(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        await self._send_with_error_handling(
            self._internal_lovelace_config, connection, msg
        )

    async def _internal_lovelace_config(
        self,
        _connection: core.WebSocket.Connection,
        msg: dict,
        config: LovelaceConfig,
    ):
        """Send Lovelace UI config over WebSocket configuration."""
        return await config.async_load(msg["force"])

    async def _lovelace_save_config(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        connection.require_admin()
        await self._send_with_error_handling(
            self._internal_lovelace_save_config, connection, msg
        )

    async def _internal_lovelace_save_config(
        self,
        _connection: core.WebSocket.Connection,
        msg: dict,
        config: LovelaceConfig,
    ):
        """Save Lovelace UI configuration."""
        await config.async_save(msg["config"])

    async def _lovelace_delete_config(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        connection.require_admin()
        await self._send_with_error_handling(
            self._internal_lovelace_delete_config, connection, msg
        )

    async def _internal_lovelace_delete_config(
        self,
        _connection: core.WebSocket.Connection,
        _msg: dict,
        config: LovelaceConfig,
    ):
        """Delete Lovelace UI configuration."""
        await config.async_delete()

    @core.callback
    def _lovelace_dashboards(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List Lovelace UI configuration."""
        connection.send_result(
            msg["id"],
            [
                dashboard.config
                for dashboard in self._dashboards.values()
                if dashboard.config
            ],
        )

    @core.callback
    def _register_panel(self, url_path: str, mode: str, config, update: bool):
        """Register a panel."""
        kwargs = {
            "frontend_url_path": url_path,
            "require_admin": config[Const.CONF_REQUIRE_ADMIN],
            "config": {"mode": mode},
            "update": update,
        }

        if config[Const.CONF_SHOW_IN_SIDEBAR]:
            kwargs["sidebar_title"] = config[Const.CONF_TITLE]
            kwargs["sidebar_icon"] = config.get(
                core.Const.CONF_ICON, Const.DEFAULT_ICON
            )

        self._frontend.async_register_built_in_panel(self.domain, **kwargs)

    def register_system_health_info(self, info: core.SystemHealthRegistration) -> None:
        """Register system health callbacks."""
        info.async_register_info(self._system_health_info, "/config/lovelace")

    async def _system_health_info(self):
        """Get info for the info page."""
        health_info = {"dashboards": len(self._dashboards)}
        health_info.update(await self._resource_collection.async_get_info())

        dashboards_info = await asyncio.gather(
            *(
                self._dashboards[dashboard].async_get_info()
                for dashboard in self._dashboards.items()
            )
        )

        modes = set()
        for dashboard in dashboards_info:
            for key in dashboard:
                if isinstance(dashboard[key], int):
                    health_info[key] = health_info.get(key, 0) + dashboard[key]
                elif key == core.Const.CONF_MODE:
                    modes.add(dashboard[key])
                else:
                    health_info[key] = dashboard[key]

        if self._mode == Const.MODE_YAML:
            health_info[core.Const.CONF_MODE] = Const.MODE_YAML
        elif Const.MODE_STORAGE in modes:
            health_info[core.Const.CONF_MODE] = Const.MODE_STORAGE
        elif Const.MODE_YAML in modes:
            health_info[core.Const.CONF_MODE] = Const.MODE_YAML
        else:
            health_info[core.Const.CONF_MODE] = Const.MODE_AUTO

        return health_info


async def _create_yaml_resource_col(shc: core.SmartHomeController, yaml_resources):
    """Create yaml resources collection."""
    if yaml_resources is None:
        default_config = LovelaceYAML(shc, None, None)
        try:
            ll_conf = await default_config.async_load(False)
        except core.SmartHomeControllerError:
            pass
        else:
            if core.Const.CONF_RESOURCES in ll_conf:
                _LOGGER.warning(
                    "Resources need to be specified in your configuration.yaml. Please see the docs"
                )
                yaml_resources = ll_conf[core.Const.CONF_RESOURCES]

    return ResourceYAMLCollection(yaml_resources or [])


def _url_slug(value: typing.Any) -> str:
    """Validate value is a valid url slug."""
    if value is None:
        raise vol.Invalid("Slug should not be None")
    if "-" not in value:
        raise vol.Invalid("Url path needs to contain a hyphen (-)")
    str_value = str(value)
    slg = core.helpers.slugify(str_value, separator="-")
    if str_value == slg:
        return str_value
    raise vol.Invalid(f"invalid slug {value} (try {slg})")
