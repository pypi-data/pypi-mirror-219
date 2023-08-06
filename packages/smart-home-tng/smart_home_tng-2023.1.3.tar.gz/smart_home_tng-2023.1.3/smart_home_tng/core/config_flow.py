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
import dataclasses
import typing

from .abort_flow import AbortFlow
from .callback import callback
from .config_entry_source import ConfigEntrySource
from .config_entry_state import ConfigEntryState
from .const import Const
from .flow_handler import FlowHandler
from .flow_result import FlowResult
from .persistent_notification_component import PersistentNotificationComponent
from .ssdp import SSDP

if not typing.TYPE_CHECKING:

    class ConfigEntry:
        ...

    class ConfigFlowPlatform:
        ...

    class SmartHomeController:
        ...

    class DhcpServiceInfo:
        ...

    class DiscoveryInfoType:
        ...

    class MqttServiceInfo:
        ...

    class UsbServiceInfo:
        ...

    class ZeroconfServiceInfo:
        ...


if typing.TYPE_CHECKING:
    from .config_entry import ConfigEntry
    from .config_flow_platform import ConfigFlowPlatform
    from .dhcp_service_info import DhcpServiceInfo
    from .discovery_info_type import DiscoveryInfoType
    from .mqtt_service_info import MqttServiceInfo
    from .smart_home_controller import SmartHomeController
    from .usb_service_info import UsbServiceInfo
    from .zeroconf_service_info import ZeroconfServiceInfo


# pylint: disable=unused-variable
class ConfigFlow(FlowHandler):
    """Base class for config flows with some helpers."""

    DEFAULT_DISCOVERY_UNIQUE_ID: typing.Final = "default_discovery_unique_id"

    def __init__(
        self,
        shc: SmartHomeController,
        handler: str,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
        version: int = 1,
    ):
        super().__init__(handler, context, data, version)
        self._shc = shc

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    @property
    def unique_id(self) -> str:
        """Return unique ID if available."""
        if not self._context:
            return None

        return typing.cast(typing.Optional[str], self._context.get("unique_id"))

    @callback
    def _async_abort_entries_match(
        self, match_dict: dict[str, typing.Any] = None
    ) -> None:
        """Abort if current entries match all data."""
        if match_dict is None:
            match_dict = {}  # Match any entry
        for entry in self._async_current_entries(include_ignore=False):
            if all(
                item in collections.ChainMap(entry.options, entry.data).items()
                for item in match_dict.items()
            ):
                raise AbortFlow("already_configured")

    @callback
    def _abort_if_unique_id_configured(
        self,
        updates: dict[str, typing.Any] = None,
        reload_on_update: bool = True,
    ) -> None:
        """Abort if the unique ID is already configured."""
        if self.unique_id is None:
            return

        for entry in self._async_current_entries(include_ignore=True):
            if entry.unique_id == self.unique_id:
                if updates is not None:
                    changed = self._shc.config_entries.async_update_entry(
                        entry, data={**entry.data, **updates}
                    )
                    if (
                        changed
                        and reload_on_update
                        and entry.state
                        in (ConfigEntryState.LOADED, ConfigEntryState.SETUP_RETRY)
                    ):
                        self._shc.async_create_task(
                            self._shc.config_entries.async_reload(entry.entry_id)
                        )
                # Allow ignored entries to be configured on manual user step
                if (
                    entry.source == ConfigEntrySource.IGNORE
                    and self.source == ConfigEntrySource.USER
                ):
                    continue
                raise AbortFlow("already_configured")

    async def async_set_unique_id(
        self, unique_id: str = None, *, raise_on_progress: bool = True
    ) -> ConfigEntry:
        """Set a unique ID for the config flow.

        Returns optionally existing config entry with same ID.
        """
        if unique_id is None:
            self._context["unique_id"] = None
            return None

        if raise_on_progress:
            for progress in self._async_in_progress(include_uninitialized=True):
                if progress["context"].get("unique_id") == unique_id:
                    raise AbortFlow("already_in_progress")

        self._context["unique_id"] = unique_id

        # Abort discoveries done using the default discovery unique id
        if unique_id != self.DEFAULT_DISCOVERY_UNIQUE_ID:
            for progress in self._async_in_progress(include_uninitialized=True):
                if (
                    progress["context"].get("unique_id")
                    == self.DEFAULT_DISCOVERY_UNIQUE_ID
                ):
                    self._shc.config_entries.flow.async_abort(progress["flow_id"])

        for entry in self._async_current_entries(include_ignore=True):
            if entry.unique_id == unique_id:
                return entry

        return None

    @callback
    def _set_confirm_only(
        self,
    ) -> None:
        """Mark the config flow as only needing user confirmation to finish flow."""
        self._context["confirm_only"] = True

    @callback
    def _async_current_entries(self, include_ignore: bool = None) -> list[ConfigEntry]:
        """Return current entries.

        If the flow is user initiated, filter out ignored entries unless include_ignore is True.
        """
        config_entries = self._shc.config_entries.async_entries(self._handler)

        if (
            include_ignore is True
            or include_ignore is None
            and self.source != ConfigEntrySource.USER
        ):
            return config_entries

        return [
            entry
            for entry in config_entries
            if entry.source != ConfigEntrySource.IGNORE
        ]

    @callback
    def _async_current_ids(self, include_ignore: bool = True) -> set[str]:
        """Return current unique IDs."""
        return {
            entry.unique_id
            for entry in self._shc.config_entries.async_entries(self._handler)
            if include_ignore or entry.source != ConfigEntrySource.IGNORE
        }

    @callback
    def _async_in_progress(
        self, include_uninitialized: bool = False
    ) -> list[FlowResult]:
        """Return other in progress flows for current domain."""
        return [
            flw
            for flw in self._shc.config_entries.flow.async_progress_by_handler(
                self._handler, include_uninitialized=include_uninitialized
            )
            if flw["flow_id"] != self._flow_id
        ]

    async def async_step_ignore(self, user_input: dict[str, typing.Any]) -> FlowResult:
        """Ignore this config flow."""
        await self.async_set_unique_id(user_input["unique_id"], raise_on_progress=False)
        return self.async_create_entry(title=user_input["title"], data={})

    async def async_step_unignore(
        self, _user_input: dict[str, typing.Any]
    ) -> FlowResult:
        """Rediscover a config entry by it's unique_id."""
        return self.async_abort(reason="not_implemented")

    async def async_step_user(
        self, _user_input: dict[str, typing.Any] = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        return self.async_abort(reason="not_implemented")

    async def _async_handle_discovery_without_unique_id(self) -> None:
        """Mark this flow discovered, without a unique identifier.

        If a flow initiated by discovery, doesn't have a unique ID, this can
        be used alternatively. It will ensure only 1 flow is started and only
        when the handler has no existing config entries.

        It ensures that the discovery can be ignored by the user.
        """
        if self.unique_id is not None:
            return

        # Abort if the handler has config entries already
        if self._async_current_entries():
            raise AbortFlow("already_configured")

        # Use an special unique id to differentiate
        await self.async_set_unique_id(self.DEFAULT_DISCOVERY_UNIQUE_ID)
        self._abort_if_unique_id_configured()

        # Abort if any other flow for this handler is already in progress
        if self._async_in_progress(include_uninitialized=True):
            raise AbortFlow("already_in_progress")

    async def async_step_discovery(
        self, _discovery_info: DiscoveryInfoType
    ) -> FlowResult:
        """Handle a flow initialized by discovery."""
        await self._async_handle_discovery_without_unique_id()
        return await self.async_step_user()

    @callback
    def async_abort(
        self, *, reason: str, description_placeholders: dict = None
    ) -> FlowResult:
        """Abort the config flow."""
        # Remove reauth notification if no reauth flows are in progress
        if self.source == ConfigEntrySource.REAUTH and not any(
            ent["context"]["source"] == ConfigEntrySource.REAUTH
            for ent in self._shc.config_entries.flow.async_progress_by_handler(
                self._handler
            )
            if ent["flow_id"] != self.flow_id
        ):
            comp = self._shc.components.persistent_notification
            if isinstance(comp, PersistentNotificationComponent):
                comp.async_dismiss(Const.CONFIG_ENTRY_RECONFIGURE_NOTIFICATION_ID)

        return super().async_abort(
            reason=reason, description_placeholders=description_placeholders
        )

    async def async_step_dhcp(self, discovery_info: DhcpServiceInfo) -> FlowResult:
        """Handle a flow initialized by DHCP discovery."""
        return await self.async_step_discovery(dataclasses.asdict(discovery_info))

    # async def async_step_hassio(
    #    self, discovery_info: HassioServiceInfo
    # ) -> FlowResult:
    #    """Handle a flow initialized by HASS IO discovery."""
    #    return await self.async_step_discovery(discovery_info.config)

    async def async_step_integration_discovery(
        self, discovery_info: DiscoveryInfoType
    ) -> FlowResult:
        """Handle a flow initialized by integration specific discovery."""
        return await self.async_step_discovery(discovery_info)

    async def async_step_homekit(
        self, discovery_info: ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle a flow initialized by Homekit discovery."""
        return await self.async_step_discovery(dataclasses.asdict(discovery_info))

    async def async_step_mqtt(self, discovery_info: MqttServiceInfo) -> FlowResult:
        """Handle a flow initialized by MQTT discovery."""
        return await self.async_step_discovery(dataclasses.asdict(discovery_info))

    async def async_step_ssdp(self, discovery_info: SSDP.ServiceInfo) -> FlowResult:
        """Handle a flow initialized by SSDP discovery."""
        return await self.async_step_discovery(dataclasses.asdict(discovery_info))

    async def async_step_usb(self, discovery_info: UsbServiceInfo) -> FlowResult:
        """Handle a flow initialized by USB discovery."""
        return await self.async_step_discovery(dataclasses.asdict(discovery_info))

    async def async_step_zeroconf(
        self, discovery_info: ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle a flow initialized by Zeroconf discovery."""
        return await self.async_step_discovery(dataclasses.asdict(discovery_info))

    @callback
    def async_create_entry(
        self,
        *,
        title: str,
        data: collections.abc.Mapping[str, typing.Any],
        description: str = None,
        description_placeholders: dict = None,
        options: collections.abc.Mapping[str, typing.Any] = None,
    ) -> FlowResult:
        """Finish config flow and create a config entry."""
        result = super().async_create_entry(
            title=title,
            data=data,
            description=description,
            description_placeholders=description_placeholders,
        )

        result["options"] = options or {}

        return result


_CONFIG_HANDLERS: typing.Final = dict[str, ConfigFlowPlatform]()
