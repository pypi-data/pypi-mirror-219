"""
Bosch SHC Integration for Smart Home - The Next Generation.

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
import os
import typing

import boschshcpy as bosch
import voluptuous as vol

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)
_HOST_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required(core.Const.CONF_HOST): str,
    }
)


def _write_tls_asset(
    comp: core.SmartHomeControllerComponent, filename: str, asset: bytes
) -> None:
    """Write the tls assets to disk."""
    os.makedirs(comp.controller.config.path(comp.domain), exist_ok=True)
    with open(
        comp.controller.config.path(comp.domain, filename), "w", encoding="utf8"
    ) as file_handle:
        file_handle.write(asset.decode("utf-8"))


def _create_credentials_and_validate(
    comp: core.SmartHomeControllerComponent, host, user_input, zeroconf_instance
):
    """Create and store credentials and validate session."""
    helper = bosch.SHCRegisterClient(host, user_input[core.Const.CONF_PASSWORD])
    result = helper.register(host, "SmartHome-TNG")

    if result is not None:
        _write_tls_asset(comp, Const.CONF_SHC_CERT, result["cert"])
        _write_tls_asset(comp, Const.CONF_SHC_KEY, result["key"])

        session = bosch.SHCSession(
            host,
            comp.controller.config.path(comp.domain, Const.CONF_SHC_CERT),
            comp.controller.config.path(comp.domain, Const.CONF_SHC_KEY),
            True,
            zeroconf_instance,
        )
        session.authenticate()

    return result


def _get_info_from_host(host, zeroconf_instance):
    """Get information from host."""
    session = bosch.SHCSession(
        host,
        "",
        "",
        True,
        zeroconf_instance,
    )
    information = session.mdns_info()
    return {"title": information.name, "unique_id": information.unique_id}


# pylint: disable=unused-variable
class BoschConfigFlow(core.ConfigFlow):
    """Handle a config flow for Bosch SHC."""

    _info = None
    _host = None
    _hostname = None

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        version = 1
        super().__init__(
            owner.controller, owner.domain, context=context, data=data, version=version
        )
        self._owner = owner
        self._zeroconf = None
        zeroconf = owner.get_component(core.Const.ZEROCONF_COMPONENT_NAME)
        if isinstance(zeroconf, core.ZeroconfComponent):
            self._zeroconf = zeroconf

    async def async_step_reauth(self, _user_input=None):
        """Perform reauth upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                data_schema=_HOST_SCHEMA,
            )
        self._host = host = user_input[core.Const.CONF_HOST]
        self._info = await self._get_info(host)
        return await self.async_step_credentials()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            host = user_input[core.Const.CONF_HOST]
            try:
                self._info = info = await self._get_info(host)
            except bosch.SHCConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info["unique_id"])
                self._abort_if_unique_id_configured({core.Const.CONF_HOST: host})
                self._host = host
                return await self.async_step_credentials()

        return self.async_show_form(
            step_id="user", data_schema=_HOST_SCHEMA, errors=errors
        )

    async def async_step_credentials(self, user_input=None):
        """Handle the credentials step."""
        errors = {}
        if user_input is not None:
            zeroconf_instance = await self._zeroconf.async_get_instance()
            try:
                result = await self._owner.controller.async_add_executor_job(
                    _create_credentials_and_validate,
                    self._owner,
                    self._host,
                    user_input,
                    zeroconf_instance,
                )
            except bosch.SHCAuthenticationError:
                errors["base"] = "invalid_auth"
            except bosch.SHCConnectionError:
                errors["base"] = "cannot_connect"
            except bosch.exceptions.SHCSessionError as err:
                _LOGGER.warning(f"Session error: {err.message}")
                errors["base"] = "session_error"
            except bosch.SHCRegistrationError as err:
                _LOGGER.warning(f"Registration error: {err.message}")
                errors["base"] = "pairing_failed"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                entry_data = {
                    Const.CONF_SSL_CERTIFICATE: self._owner.controller.config.path(
                        self._owner.domain, Const.CONF_SHC_CERT
                    ),
                    Const.CONF_SSL_KEY: self._owner.controller.config.path(
                        self._owner.domain, Const.CONF_SHC_KEY
                    ),
                    core.Const.CONF_HOST: self._host,
                    core.Const.CONF_TOKEN: result["token"],
                    Const.CONF_HOSTNAME: result["token"].split(":", 1)[1],
                }
                existing_entry = await self.async_set_unique_id(self._info["unique_id"])
                if existing_entry:
                    self._owner.controller.config_entries.async_update_entry(
                        existing_entry,
                        data=entry_data,
                    )
                    await self._owner.controller.config_entries.async_reload(
                        existing_entry.entry_id
                    )
                    return self.async_abort(reason="reauth_successful")

                return self.async_create_entry(
                    title=self._info["title"],
                    data=entry_data,
                )
        else:
            user_input = {}

        schema = vol.Schema(
            {
                vol.Required(
                    core.Const.CONF_PASSWORD,
                    default=user_input.get(core.Const.CONF_PASSWORD, ""),
                ): str,
            }
        )

        return self.async_show_form(
            step_id="credentials", data_schema=schema, errors=errors
        )

    async def async_step_zeroconf(
        self, discovery_info: core.ZeroconfServiceInfo
    ) -> core.FlowResult:
        """Handle zeroconf discovery."""
        if not discovery_info.name.startswith("Bosch SHC"):
            return self.async_abort(reason="not_bosch_shc")

        try:
            self._info = await self._get_info(discovery_info.host)
        except bosch.SHCConnectionError:
            return self.async_abort(reason="cannot_connect")
        self._host = discovery_info.host

        local_name = discovery_info.hostname[:-1]
        node_name = local_name[: -len(".local")]

        await self.async_set_unique_id(self._info["unique_id"])
        self._abort_if_unique_id_configured({core.Const.CONF_HOST: self._host})
        self.context["title_placeholders"] = {"name": node_name}
        return await self.async_step_confirm_discovery()

    async def async_step_confirm_discovery(self, user_input=None):
        """Handle discovery confirm."""
        errors = {}
        if user_input is not None:
            return await self.async_step_credentials()

        return self.async_show_form(
            step_id="confirm_discovery",
            description_placeholders={
                "model": "Bosch SHC",
                "host": self._host,
            },
            errors=errors,
        )

    async def _get_info(self, host):
        """Get additional information."""
        zeroconf_instance = await self._zeroconf.async_get_instance()

        return await self._owner.controller.async_add_executor_job(
            _get_info_from_host,
            host,
            zeroconf_instance,
        )
