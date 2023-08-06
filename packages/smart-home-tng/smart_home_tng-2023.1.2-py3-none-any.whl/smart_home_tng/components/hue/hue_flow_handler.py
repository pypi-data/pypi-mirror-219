"""
Philips Hue Integration for Smart Home - The Next Generation.

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
import urllib.parse

import aiohttp
import aiohue
import async_timeout
import slugify
import voluptuous as vol
from aiohue import discovery

from ... import core
from .const import Const

_ssdp: typing.TypeAlias = core.SSDP
_HUE_MANUFACTURERURL: typing.Final = (
    "http://www.philips.com",
    "http://www.philips-hue.com",
)
_HUE_IGNORED_BRIDGE_NAMES: typing.Final = ["Home Assistant Bridge", "Espalexa"]
_HUE_MANUAL_BRIDGE_ID: typing.Final = "manual"
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class HueFlowHandler(core.ConfigFlow):
    """Handle a Hue config flow."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        """Initialize the Hue flow."""
        super().__init__(owner.controller, owner.domain, context, data)
        self._bridge: discovery.DiscoveredHueBridge = None
        self._discovered_bridges: dict[str, discovery.DiscoveredHueBridge] = None
        self._owner = owner

    async def async_step_user(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle a flow initialized by the user."""
        # This is for backwards compatibility.
        return await self.async_step_init(user_input)

    async def _get_bridge(
        self, host: str, bridge_id: str = None
    ) -> discovery.DiscoveredHueBridge:
        """Return a DiscoveredHueBridge object."""
        try:
            bridge = await discovery.discover_bridge(
                host, websession=core.HttpClient.async_get_clientsession(self._shc)
            )
        except aiohttp.ClientError:
            return None
        if bridge_id is not None:
            bridge_id = aiohue.util.normalize_bridge_id(bridge_id)
            assert bridge_id == bridge.id
        return bridge

    async def async_step_init(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle a flow start."""
        # Check if user chooses manual entry
        if user_input is not None and user_input["id"] == _HUE_MANUAL_BRIDGE_ID:
            return await self.async_step_manual()

        if (
            user_input is not None
            and self._discovered_bridges is not None
            and user_input["id"] in self._discovered_bridges
        ):
            self._bridge = self._discovered_bridges[user_input["id"]]
            await self.async_set_unique_id(self._bridge.id, raise_on_progress=False)
            return await self.async_step_link()

        # Find / discover bridges
        try:
            async with async_timeout.timeout(5):
                bridges = await discovery.discover_nupnp(
                    websession=core.HttpClient.async_get_clientsession(self._shc)
                )
        except asyncio.TimeoutError:
            return self.async_abort(reason="discover_timeout")

        if bridges:
            # Find already configured hosts
            already_configured = self._async_current_ids(False)
            bridges = [
                bridge for bridge in bridges if bridge.id not in already_configured
            ]
            self._discovered_bridges = {bridge.id: bridge for bridge in bridges}

        if not self._discovered_bridges:
            return await self.async_step_manual()

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required("id"): vol.In(
                        {
                            **{bridge.id: bridge.host for bridge in bridges},
                            _HUE_MANUAL_BRIDGE_ID: "Manually add a Hue Bridge",
                        }
                    )
                }
            ),
        )

    async def async_step_manual(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle manual bridge setup."""
        if user_input is None:
            return self.async_show_form(
                step_id="manual",
                data_schema=vol.Schema({vol.Required(core.Const.CONF_HOST): str}),
            )

        self._async_abort_entries_match({"host": user_input["host"]})
        self._bridge = await self._get_bridge(user_input[core.Const.CONF_HOST])
        return await self.async_step_link()

    async def async_step_link(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Attempt to link with the Hue bridge.

        Given a configured host, will ask the user to press the link button
        to connect to the bridge.
        """
        if user_input is None:
            return self.async_show_form(step_id="link")

        bridge = self._bridge
        assert bridge is not None
        errors = {}
        device_name = slugify.slugify(self._shc.config.location_name, max_length=19)

        try:
            app_key = await aiohue.create_app_key(
                bridge.host,
                f"smart-home-tng#{device_name}",
                websession=core.HttpClient.async_get_clientsession(self._shc),
            )
        except aiohue.LinkButtonNotPressed:
            errors["base"] = "register_failed"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                f"Unknown error connecting with Hue bridge at {bridge.host}"
            )
            errors["base"] = "linking"

        if errors:
            return self.async_show_form(step_id="link", errors=errors)

        # Can happen if we come from import or manual entry
        if self.unique_id is None:
            await self.async_set_unique_id(
                aiohue.util.normalize_bridge_id(bridge.id), raise_on_progress=False
            )

        return self.async_create_entry(
            title=f"Hue Bridge {bridge.id}",
            data={
                core.Const.CONF_HOST: bridge.host,
                core.Const.CONF_API_KEY: app_key,
                Const.CONF_API_VERSION: 2 if bridge.supports_v2 else 1,
            },
        )

    async def async_step_ssdp(
        self, discovery_info: _ssdp.ServiceInfo
    ) -> core.FlowResult:
        """Handle a discovered Hue bridge.

        This flow is triggered by the SSDP component. It will check if the
        host is already configured and delegate to the import step if not.
        """
        # Filter out non-Hue bridges #1
        if (
            discovery_info.upnp.get(_ssdp.ATTR_UPNP_MANUFACTURER_URL)
            not in _HUE_MANUFACTURERURL
        ):
            return self.async_abort(reason="not_hue_bridge")

        # Filter out non-Hue bridges #2
        if any(
            name in discovery_info.upnp.get(_ssdp.ATTR_UPNP_FRIENDLY_NAME, "")
            for name in _HUE_IGNORED_BRIDGE_NAMES
        ):
            return self.async_abort(reason="not_hue_bridge")

        if (
            not discovery_info.ssdp_location
            or _ssdp.ATTR_UPNP_SERIAL not in discovery_info.upnp
        ):
            return self.async_abort(reason="not_hue_bridge")

        url = urllib.parse.urlparse(discovery_info.ssdp_location)
        if not url.hostname:
            return self.async_abort(reason="not_hue_bridge")

        # Ignore if host is IPv6
        if core.helpers.is_ipv6_address(url.hostname):
            return self.async_abort(reason="invalid_host")

        # abort if we already have exactly this bridge id/host
        # reload the integration if the host got updated
        bridge_id = aiohue.util.normalize_bridge_id(
            discovery_info.upnp[_ssdp.ATTR_UPNP_SERIAL]
        )
        await self.async_set_unique_id(bridge_id)
        self._abort_if_unique_id_configured(
            updates={core.Const.CONF_HOST: url.hostname}, reload_on_update=True
        )

        self._bridge = await self._get_bridge(
            url.hostname, discovery_info.upnp[_ssdp.ATTR_UPNP_SERIAL]
        )
        return await self.async_step_link()

    async def async_step_zeroconf(
        self, discovery_info: core.ZeroconfServiceInfo
    ) -> core.FlowResult:
        """Handle a discovered Hue bridge.

        This flow is triggered by the Zeroconf component. It will check if the
        host is already configured and delegate to the import step if not.
        """
        # Ignore if host is IPv6
        if core.helpers.is_ipv6_address(discovery_info.host):
            return self.async_abort(reason="invalid_host")

        # abort if we already have exactly this bridge id/host
        # reload the integration if the host got updated
        bridge_id = aiohue.util.normalize_bridge_id(
            discovery_info.properties["bridgeid"]
        )
        await self.async_set_unique_id(bridge_id)
        self._abort_if_unique_id_configured(
            updates={core.Const.CONF_HOST: discovery_info.host}, reload_on_update=True
        )

        # we need to query the other capabilities too
        self._bridge = await self._get_bridge(
            discovery_info.host, discovery_info.properties["bridgeid"]
        )
        return await self.async_step_link()

    async def async_step_homekit(
        self, discovery_info: core.ZeroconfServiceInfo
    ) -> core.FlowResult:
        """Handle a discovered Hue bridge on HomeKit.

        The bridge ID communicated over HomeKit differs, so we cannot use that
        as the unique identifier. Therefore, this method uses discovery without
        a unique ID.
        """
        self._bridge = await self._get_bridge(discovery_info.host)
        await self._async_handle_discovery_without_unique_id()
        return await self.async_step_link()

    async def async_step_import(
        self, import_info: dict[str, typing.Any]
    ) -> core.FlowResult:
        """Import a new bridge as a config entry.

        This flow is triggered by `async_setup` for both configured and
        discovered bridges. Triggered for any bridge that does not have a
        config entry yet (based on host).

        This flow is also triggered by `async_step_discovery`.
        """
        # Check if host exists, abort if so.
        self._async_abort_entries_match({"host": import_info["host"]})

        self._bridge = await self._get_bridge(import_info["host"])
        return await self.async_step_link()
