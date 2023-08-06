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

import http

import voluptuous_serialize

from ... import auth, core


# pylint: disable=unused-variable
class LoginFlowBaseView(core.SmartHomeControllerView):
    """Base class for the login views."""

    def __init__(
        self,
        flow_mgr,
        store_result,
        url: str = None,
        name: str = None,
        extra_urls: list[str] = None,
        cors_allowed=False,
    ):
        """Initialize the flow manager index view."""
        super().__init__(
            url,
            name,
            extra_urls=extra_urls,
            cors_allowed=cors_allowed,
            requires_auth=False,
        )
        self._flow_mgr = flow_mgr
        self._store_result = store_result

    async def _async_flow_result_to_response(self, request, client_id, result):
        """Convert the flow result to a response."""
        if result["type"] != core.FlowResultType.CREATE_ENTRY:
            # @log_invalid_auth does not work here since it returns HTTP 200.
            # We need to manually log failed login attempts.
            if (
                result["type"] == core.FlowResultType.FORM
                and (errors := result.get("errors"))
                and errors.get("base")
                in (
                    "invalid_auth",
                    "invalid_code",
                )
            ):
                shc = request.app[core.Const.KEY_SHC]
                await shc.http.process_wrong_login(request)
            return self.json(_prepare_result_json(result))

        result.pop("data")

        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]
        result_obj: auth.Credentials = result.pop("result")

        # Result can be None if credential was never linked to a user before.
        user = await shc.auth.async_get_user_by_credentials(result_obj)

        if user is not None and (
            user_access_error := shc.http.async_user_not_allowed_do_auth(user)
        ):
            return self.json_message(
                f"Login blocked: {user_access_error}", http.HTTPStatus.FORBIDDEN
            )

        await shc.http.process_success_login(request)
        result["result"] = self._store_result(client_id, result_obj)

        return self.json(result)


def _prepare_result_json(result):
    """Convert result to JSON."""
    if result["type"] == core.FlowResultType.CREATE_ENTRY:
        data = result.copy()
        data.pop("result")
        data.pop("data")
        return data

    if result["type"] != core.FlowResultType.FORM:
        return result

    data = result.copy()

    if (schema := data["data_schema"]) is None:
        data["data_schema"] = []
    else:
        data["data_schema"] = voluptuous_serialize.convert(schema)

    return data
