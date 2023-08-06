"""
Diagnostics Component for Smart Home - The Next Generation.

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
import json
import logging
import typing

from aiohttp import web

from ... import core
from .diagnostic_platforms import _DIAGNOSTIC_PLATFORMS

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class DownloadDiagnosticsView(core.SmartHomeControllerView):
    """Download diagnostics view."""

    def __init__(self):
        url = "/api/diagnostics/{d_type}/{d_id}"
        extra_urls = ["/api/diagnostics/{d_type}/{d_id}/{sub_type}/{sub_id}"]
        name = "api:diagnostics"
        super().__init__(url, name, extra_urls)

    async def get(
        self,
        request: web.Request,
        d_type: str,
        d_id: str,
        sub_type: str = None,
        sub_id: str = None,
    ) -> web.Response:
        """Download diagnostics."""
        # t_type handling
        try:
            diagnostic_type = core.Diagnostics.Type(d_type)
        except ValueError:
            return web.Response(status=http.HTTPStatus.BAD_REQUEST)

        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]

        if (config_entry := shc.config_entries.async_get_entry(d_id)) is None:
            return web.Response(status=http.HTTPStatus.NOT_FOUND)

        if (platform := _DIAGNOSTIC_PLATFORMS.get(config_entry.domain)) is None:
            return web.Response(status=http.HTTPStatus.NOT_FOUND)

        filename = f"{config_entry.domain}-{config_entry.entry_id}"

        if sub_type is None:
            if not platform.supports_config_entry_diagnostics:
                return web.Response(status=http.HTTPStatus.NOT_FOUND)
            data = await platform.async_get_config_entry_diagnostics(config_entry)
            filename = f"{diagnostic_type}-{filename}"
            return await _async_get_json_file_response(
                shc,
                data,
                filename,
                config_entry.domain,
                diagnostic_type.value,
                d_id,
            )

        # sub_type handling
        try:
            sub_type = core.Diagnostics.SubType(sub_type)
        except ValueError:
            return web.Response(status=http.HTTPStatus.BAD_REQUEST)

        dev_reg = shc.device_registry
        assert sub_id

        if (device := dev_reg.async_get(sub_id)) is None:
            return web.Response(status=http.HTTPStatus.NOT_FOUND)

        filename += f"-{device.name}-{device.id}"

        if not platform.support_device_diagnostic:
            return web.Response(status=http.HTTPStatus.NOT_FOUND)
        data = await platform.async_get_device_diagnostics(config_entry, device)

        return await _async_get_json_file_response(
            shc,
            data,
            filename,
            config_entry.domain,
            diagnostic_type,
            d_id,
            sub_type,
            sub_id,
        )


async def _async_get_json_file_response(
    shc: core.SmartHomeController,
    data: typing.Any,
    filename: str,
    domain: str,
    diagnostic_type: core.Diagnostics.Type,
    config_entry_id: str,
    sub_type: core.Diagnostics.SubType = None,
    sub_id: str = None,
) -> web.Response:
    """Return JSON file from dictionary."""
    shc_sys_info = await core.helpers.async_get_system_info(shc)
    shc_sys_info["run_as_root"] = shc_sys_info["user"] == "root"
    del shc_sys_info["user"]

    integration = await shc.setup.async_get_integration(domain)
    custom_components = {}
    all_custom_components = await shc.setup.async_get_custom_components()
    for cc_domain, cc_obj in all_custom_components.items():
        custom_components[cc_domain] = {
            "version": cc_obj.version,
            "requirements": cc_obj.requirements,
        }
    try:
        json_data = json.dumps(
            {
                "smart_home_tng": shc_sys_info,
                "custom_components": custom_components,
                "integration_manifest": integration.manifest,
                "data": data,
            },
            indent=2,
            cls=core.ExtendedJsonEncoder,
        )
    except TypeError:
        sub_msg = f"/{sub_type.value}/{sub_id}" if sub_type is not None else ""
        pos = core.helpers.format_unserializable_data(
            core.helpers.find_paths_unserializable_data(data)
        )
        _LOGGER.error(
            f"Failed to serialize to JSON: {diagnostic_type.value}/{config_entry_id}"
            + f"{sub_msg}. Bad data at {pos}",
        )
        return web.Response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return web.Response(
        body=json_data,
        content_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}.json.txt"'},
    )
