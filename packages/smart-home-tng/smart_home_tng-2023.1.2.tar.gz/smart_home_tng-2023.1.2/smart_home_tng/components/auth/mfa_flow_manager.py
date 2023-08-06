"""
Auth Component for Smart Home - The Next Generation.

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
import voluptuous_serialize

from ... import core

_WS_TYPE_SETUP_MFA: typing.Final = "auth/setup_mfa"
_WS_SETUP_MFA: typing.Final = {
    vol.Required("type"): _WS_TYPE_SETUP_MFA,
    vol.Exclusive("mfa_module_id", "module_or_flow_id"): str,
    vol.Exclusive("flow_id", "module_or_flow_id"): str,
    vol.Optional("user_input"): object,
}

_WS_TYPE_DEPOSE_MFA: typing.Final = "auth/depose_mfa"
_WS_DEPOSE_MFA: typing.Final = {
    vol.Required("type"): _WS_TYPE_DEPOSE_MFA,
    vol.Required("mfa_module_id"): str,
}
_LOGGER = logging.getLogger(__name__)


class MfaFlowManager(core.FlowManager):
    """Manage multi factor authentication flows."""

    async def async_create_flow(self, handler_key, *, context, data):
        """Create a setup flow. handler is a mfa module."""
        mfa_module = self._shc.auth.get_auth_mfa_module(handler_key)
        if mfa_module is None:
            raise ValueError(f"Mfa module {handler_key} is not found")

        user_id = data.pop("user_id")
        return await mfa_module.async_setup_flow(user_id)

    async def async_finish_flow(self, _flow, result):
        """Complete an mfs setup flow."""
        _LOGGER.debug(f"flow_result: {result}")
        return result

    @staticmethod
    async def async_setup(websocket_api: core.WebSocket.Component):
        """Init mfa setup flow manager."""
        MfaFlowManager._flow_manager = MfaFlowManager(websocket_api.controller)

        websocket_api.register_command(_WS_TYPE_SETUP_MFA, _WS_SETUP_MFA, _setup_mfa)

        websocket_api.register_command(_WS_TYPE_DEPOSE_MFA, _WS_DEPOSE_MFA, _depose_mfa)

    async def async_post_init(
        self, _flow: core.FlowHandler, _result: core.FlowResult
    ) -> None:
        return

    _flow_manager: "MfaFlowManager" = None


@core.callback
def _setup_mfa(connection: core.WebSocket.Connection, msg: dict):
    """Return a setup flow for mfa auth module."""
    if not connection.check_user(msg["id"], allow_system_user=False):
        return

    async def async_setup_flow(msg):
        """Return a setup flow for mfa auth module."""
        # pylint: disable=protected-access
        flow_manager = MfaFlowManager._flow_manager

        if (flow_id := msg.get("flow_id")) is not None:
            result = await flow_manager.async_configure(flow_id, msg.get("user_input"))
            connection.send_result(msg["id"], _prepare_result_json(result))
            return

        mfa_module_id = msg.get("mfa_module_id")
        mfa_module = connection.owner.controller.auth.get_auth_mfa_module(mfa_module_id)
        if mfa_module is None:
            connection.send_error(
                msg["id"], "no_module", f"MFA module {mfa_module_id} is not found"
            )
            return

        result = await flow_manager.async_init(
            mfa_module_id, data={"user_id": connection.user.id}
        )

        connection.send_result(msg["id"], _prepare_result_json(result))

    connection.owner.controller.async_create_task(async_setup_flow(msg))


@core.callback
def _depose_mfa(connection: core.WebSocket.Connection, msg: dict):
    """Remove user from mfa module."""
    if not connection.check_user(msg["id"], allow_system_user=False):
        return

    async def async_depose(msg):
        """Remove user from mfa auth module."""
        mfa_module_id = msg["mfa_module_id"]
        try:
            await connection.owner.controller.auth.async_disable_user_mfa(
                connection.user, msg["mfa_module_id"]
            )
        except ValueError as err:
            connection.send_error(
                msg["id"],
                "disable_failed",
                f"Cannot disable MFA Module {mfa_module_id}: {err}",
            )
            return

        connection.send_result(msg["id"], "done")

    connection.owner.controller.async_create_task(async_depose(msg))


def _prepare_result_json(result):
    """Convert result to JSON."""
    if result["type"] == core.FlowResultType.CREATE_ENTRY:
        data = result.copy()
        return data

    if result["type"] != core.FlowResultType.FORM:
        return result

    data = result.copy()

    if (schema := data["data_schema"]) is None:
        data["data_schema"] = []
    else:
        data["data_schema"] = voluptuous_serialize.convert(schema)

    return data
