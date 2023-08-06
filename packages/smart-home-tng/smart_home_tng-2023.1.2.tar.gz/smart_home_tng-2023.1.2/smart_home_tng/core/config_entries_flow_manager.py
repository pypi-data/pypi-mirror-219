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

import logging
import typing

from .callback import callback
from .config_entry import ConfigEntry
from .config_entry_source import ConfigEntrySource
from .config_flow import ConfigFlow, _CONFIG_HANDLERS
from .config_flow_platform import ConfigFlowPlatform
from .config_type import ConfigType
from .const import Const
from .flow_handler import FlowHandler
from .flow_manager import FlowManager
from .flow_result import FlowResult
from .flow_result_type import FlowResultType
from .integration_not_found import IntegrationNotFound
from .persistent_notification_component import PersistentNotificationComponent
from .platform import Platform
from .smart_home_controller_component import SmartHomeControllerComponent
from .unknown_handler import UnknownHandler


if not typing.TYPE_CHECKING:

    class ConfigEntries:
        ...

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .config_entries import ConfigEntries
    from .smart_home_controller import SmartHomeController


_DISCOVERY_SOURCES: typing.Final = (
    ConfigEntrySource.DHCP,
    ConfigEntrySource.DISCOVERY,
    ConfigEntrySource.HOMEKIT,
    ConfigEntrySource.IMPORT,
    ConfigEntrySource.INTEGRATION_DISCOVERY,
    ConfigEntrySource.MQTT,
    ConfigEntrySource.SSDP,
    ConfigEntrySource.UNIGNORE,
    ConfigEntrySource.USB,
    ConfigEntrySource.ZEROCONF,
)

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class ConfigEntriesFlowManager(FlowManager):
    """Manage all the config entry flows that are in progress."""

    def __init__(
        self,
        shc: SmartHomeController,
        config_entries: ConfigEntries,
        config: ConfigType,
    ) -> None:
        """Initialize the config entry flow manager."""
        super().__init__(shc)
        self._config_entries = config_entries
        self._config = config

    @callback
    def _async_has_other_discovery_flows(self, flow_id: str) -> bool:
        """Check if there are any other discovery flows in progress."""
        return any(
            flow.context["source"] in _DISCOVERY_SOURCES and flow.flow_id != flow_id
            for flow in self._progress.values()
        )

    async def async_finish_flow(
        self, flow: FlowHandler, result: FlowResult
    ) -> FlowResult:
        """Finish a config flow and add an entry."""
        flow = typing.cast(ConfigFlow, flow)

        # Remove notification if no other discovery config entries in progress
        if not self._async_has_other_discovery_flows(flow.flow_id):
            comp = SmartHomeControllerComponent.get_component(
                Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
            )
            if isinstance(comp, PersistentNotificationComponent):
                comp.async_dismiss(ConfigEntry.DISCOVERY_NOTIFICATION_ID)

        if result["type"] != FlowResultType.CREATE_ENTRY:
            return result

        # Check if config entry exists with unique ID. Unload it.
        existing_entry = None

        # Abort all flows in progress with same unique ID
        # or the default discovery ID
        for progress_flow in self.async_progress_by_handler(flow.handler):
            progress_unique_id = progress_flow["context"].get("unique_id")
            if progress_flow["flow_id"] != flow.flow_id and (
                (flow.unique_id and progress_unique_id == flow.unique_id)
                or progress_unique_id == ConfigFlow.DEFAULT_DISCOVERY_UNIQUE_ID
            ):
                self.async_abort(progress_flow["flow_id"])

        if flow.unique_id is not None:
            # Reset unique ID when the default discovery ID has been used
            if flow.unique_id == ConfigFlow.DEFAULT_DISCOVERY_UNIQUE_ID:
                await flow.async_set_unique_id(None)

            # Find existing entry.
            for check_entry in self._config_entries.async_entries(result["handler"]):
                if check_entry.unique_id == flow.unique_id:
                    existing_entry = check_entry
                    break

        # Unload the entry before setting up the new one.
        # We will remove it only after the other one is set up,
        # so that device customizations are not getting lost.
        if existing_entry is not None and existing_entry.state.recoverable:
            await self._config_entries.async_unload(existing_entry.entry_id)

        entry = ConfigEntry(
            version=result["version"],
            domain=result["handler"],
            title=result["title"],
            data=result["data"],
            options=result["options"],
            source=flow.context["source"],
            unique_id=flow.unique_id,
        )

        await self._config_entries.async_add(entry)

        if existing_entry is not None:
            await self._config_entries.async_remove(existing_entry.entry_id)

        result["result"] = entry
        return result

    async def async_create_flow(
        self,
        handler_key: typing.Any,
        *,
        context: dict = None,
        data: typing.Any = None,
    ) -> FlowHandler:
        """Create a flow for specified handler.

        Handler key is the domain of the component that we want to set up.
        """
        try:
            integration = await self._shc.setup.async_get_integration(handler_key)
        except IntegrationNotFound as err:
            _LOGGER.error(f"Cannot find integration {handler_key}")
            raise UnknownHandler from err

        # Make sure requirements and dependencies of component are resolved
        await self._shc.setup.async_process_deps_reqs(self._config, integration)

        integration.get_component()

        platform = _CONFIG_HANDLERS.get(handler_key)
        if platform is None:
            comp = SmartHomeControllerComponent.get_component(handler_key)
            if isinstance(comp, SmartHomeControllerComponent):
                platform = comp.get_platform(Platform.CONFIG_FLOW)
                if not isinstance(platform, ConfigFlowPlatform):
                    platform = None
        if platform is None:
            raise UnknownHandler

        if not context or "source" not in context:
            raise KeyError("Context not set or doesn't have a source set")

        return platform.create_config_flow(context, data)

    async def async_post_init(self, flow: FlowHandler, result: FlowResult) -> None:
        """After a flow is initialised trigger new flow notifications."""
        source = flow.context["source"]
        comp = SmartHomeControllerComponent.get_component(
            Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
        )
        if not isinstance(comp, PersistentNotificationComponent):
            comp = None

        # Create notification.
        if source in _DISCOVERY_SOURCES:
            self._shc.bus.async_fire(ConfigEntry.EVENT_FLOW_DISCOVERED)
            if comp is not None:
                comp.async_create(
                    "Wir haben neue Geräte in deinem Netzwerk entdeckt. "
                    + "[Überprüfen](/config/integrations).",
                    "Neue Geräte entdeckt",
                    ConfigEntry.DISCOVERY_NOTIFICATION_ID,
                )
        elif source == ConfigEntrySource.REAUTH:
            if comp is not None:
                comp.async_create(
                    "Mindestens eine deiner Integrationen muss neu konfiguriert "
                    + "werden, um weiter zu funktionieren. "
                    + "[Überprüfen](/config/integrations).",
                    "Integration erfordert Rekonfiguration",
                    Const.CONFIG_ENTRY_RECONFIGURE_NOTIFICATION_ID,
                )
