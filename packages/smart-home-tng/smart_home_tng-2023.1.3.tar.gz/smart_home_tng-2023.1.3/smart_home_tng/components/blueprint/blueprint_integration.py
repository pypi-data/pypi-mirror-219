"""
Automation Integration for Smart Home - The Next Generation.

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

import async_timeout
import voluptuous as vol

from ... import core
from .helpers import is_blueprint_instance_config, fetch_blueprint_from_url
from .blueprint import Blueprint
from .domain_blueprints import DomainBlueprints
from .file_already_exists import FileAlreadyExists

_cv: typing.TypeAlias = core.ConfigValidation

_DOMAIN_BLUEPRINTS: typing.Final = dict[str, DomainBlueprints]()

_LIST_BLUEPRINTS: typing.Final = {
    vol.Required("type"): "blueprint/list",
    vol.Required("domain"): _cv.string,
}
_IMPORT_BLUEPRINT: typing.Final = {
    vol.Required("type"): "blueprint/import",
    vol.Required("url"): _cv.url,
}
_SAVE_BLUEPRRINT: typing.Final = {
    vol.Required("type"): "blueprint/save",
    vol.Required("domain"): _cv.string,
    vol.Required("path"): _cv.path,
    vol.Required("yaml"): _cv.string,
    vol.Optional("source_url"): _cv.url,
}
_DELETE_BLUEPRINT: typing.Final = {
    vol.Required("type"): "blueprint/delete",
    vol.Required("domain"): _cv.string,
    vol.Required("path"): _cv.path,
}


# pylint: disable=unused-variable
class BlueprintIntegration(core.BlueprintComponent):
    """The blueprint integration."""

    def create_domain_blueprints(
        self, domain: str, logger: logging.Logger
    ) -> core.DomainBlueprintsBase:
        """Create a new DomainBlueprints instance."""
        result = DomainBlueprints(self._shc, domain, logger)
        _DOMAIN_BLUEPRINTS[domain] = result
        return result

    @core.callback
    def is_blueprint_instance_config(self, config: typing.Any) -> bool:
        """Return if it is a blueprint instance config."""
        return is_blueprint_instance_config(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the websocket API."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        api.register_command(self._list_blueprints, _LIST_BLUEPRINTS)
        api.register_command(self._import_blueprint, _IMPORT_BLUEPRINT)
        api.register_command(self._save_blueprint, _SAVE_BLUEPRRINT)
        api.register_command(self._delete_blueprint, _DELETE_BLUEPRINT)
        return True

    async def _list_blueprints(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List available blueprints."""
        results = {}

        if msg["domain"] not in _DOMAIN_BLUEPRINTS:
            connection.send_result(msg["id"], results)
            return

        domain_results = await _DOMAIN_BLUEPRINTS[msg["domain"]].async_get_blueprints()

        for path, value in domain_results.items():
            if isinstance(value, Blueprint):
                results[path] = {
                    "metadata": value.metadata,
                }
            else:
                results[path] = {"error": str(value)}

        connection.send_result(msg["id"], results)

    async def _import_blueprint(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Import a blueprint."""
        shc = connection.owner.controller

        async with async_timeout.timeout(10):
            imported_blueprint = await fetch_blueprint_from_url(shc, msg["url"])

        if imported_blueprint is None:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_NOT_SUPPORTED,
                "This url is not supported",
            )
            return

        connection.send_result(
            msg["id"],
            {
                "suggested_filename": imported_blueprint.suggested_filename,
                "raw_data": imported_blueprint.raw_data,
                "blueprint": {
                    "metadata": imported_blueprint.blueprint.metadata,
                },
                "validation_errors": imported_blueprint.blueprint.validate(),
            },
        )

    async def _save_blueprint(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Save a blueprint."""

        path = msg["path"]
        domain = msg["domain"]

        if domain not in _DOMAIN_BLUEPRINTS:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_INVALID_FORMAT, "Unsupported domain"
            )

        try:
            blueprint = Blueprint(
                core.YamlLoader.parse_yaml(msg["yaml"]), expected_domain=domain
            )
            if "source_url" in msg:
                blueprint.update_metadata(source_url=msg["source_url"])
        except core.SmartHomeControllerError as err:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_INVALID_FORMAT, str(err)
            )
            return

        try:
            await _DOMAIN_BLUEPRINTS[domain].async_add_blueprint(blueprint, path)
        except FileAlreadyExists:
            connection.send_error(msg["id"], "already_exists", "File already exists")
            return
        except OSError as err:
            connection.send_error(msg["id"], core.WebSocket.ERR_UNKNOWN_ERROR, str(err))
            return

        connection.send_result(
            msg["id"],
        )

    async def _delete_blueprint(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Delete a blueprint."""

        path = msg["path"]
        domain = msg["domain"]

        if domain not in _DOMAIN_BLUEPRINTS:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_INVALID_FORMAT, "Unsupported domain"
            )

        try:
            await _DOMAIN_BLUEPRINTS[domain].async_remove_blueprint(path)
        except OSError as err:
            connection.send_error(msg["id"], core.WebSocket.ERR_UNKNOWN_ERROR, str(err))
            return

        connection.send_result(
            msg["id"],
        )
