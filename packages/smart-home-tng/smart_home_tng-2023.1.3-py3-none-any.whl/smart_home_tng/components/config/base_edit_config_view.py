"""
Configuration API for Smart Home - The Next Generation.

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
import collections.abc
import http
import os
import pathlib
import typing

import voluptuous as vol

from ... import core

_ACTION_CREATE_UPDATE: typing.Final = "create_update"
_ACTION_DELETE: typing.Final = "delete"


# pylint: disable=unused-variable
class BaseEditConfigView(core.SmartHomeControllerView):
    """Configure a Group endpoint."""

    ACTION_DELETE: typing.Final = _ACTION_DELETE
    ACTION_CREATE_UPDATE: typing.Final = _ACTION_CREATE_UPDATE

    def __init__(
        self,
        component: str,
        config_type: str,
        path: str,
        key_schema: collections.abc.Callable[[core.JsonType], core.ConfigType],
        data_schema: collections.abc.Callable[[core.JsonType], core.ConfigType],
        *,
        post_write_hook: collections.abc.Callable[[str, str], None] = None,
        data_validator: collections.abc.Callable[
            [core.JsonType], core.ConfigType
        ] = None,
    ):
        """Initialize a config view."""
        super().__init__(
            f"/api/config/{component}/{config_type}/{{config_key}}",
            f"api:config:{component}:{config_type}",
        )
        self._path = path
        self._key_schema = key_schema
        self._data_schema = data_schema
        self._post_write_hook = post_write_hook
        self._data_validator = data_validator
        self._mutation_lock = asyncio.Lock()

    def _empty_config(self):
        """Empty config if file not found."""
        raise NotImplementedError()

    def _get_value(
        self, shc: core.SmartHomeController, data: core.JsonType, config_key: str
    ):
        """Get value."""
        raise NotImplementedError()

    def _write_value(
        self,
        shc: core.SmartHomeController,
        data: core.JsonType,
        config_key: str,
        new_value: core.JsonType,
    ):
        """Set value."""
        raise NotImplementedError()

    def _delete_value(
        self, shc: core.SmartHomeController, data: core.JsonType, config_key: str
    ):
        """Delete value."""
        raise NotImplementedError()

    async def get(self, request, config_key: str):
        """Fetch device specific config."""
        shc = request.app[core.Const.KEY_SHC]
        async with self._mutation_lock:
            current = await self.read_config(shc)
            value = self._get_value(shc, current, config_key)

        if value is None:
            return self.json_message("Resource not found", http.HTTPStatus.NOT_FOUND)

        return self.json(value)

    async def post(self, request, config_key: str):
        """Validate config and return results."""
        try:
            data = await request.json()
        except ValueError:
            return self.json_message(
                "Invalid JSON specified", http.HTTPStatus.BAD_REQUEST
            )

        try:
            self._key_schema(config_key)
        except vol.Invalid as err:
            return self.json_message(
                f"Key malformed: {err}", http.HTTPStatus.BAD_REQUEST
            )

        shc = request.app[core.Const.KEY_SHC]

        try:
            # We just validate, we don't store that data because
            # we don't want to store the defaults.
            if self._data_validator:
                await self._data_validator(data)
            else:
                self._data_schema(data)
        except (vol.Invalid, core.SmartHomeControllerError) as err:
            return self.json_message(
                f"Message malformed: {err}", http.HTTPStatus.BAD_REQUEST
            )

        path = shc.config.path(self._path)

        async with self._mutation_lock:
            current = await self.read_config(shc)
            self._write_value(shc, current, config_key, data)

            await shc.async_add_executor_job(_write, path, current)

        if self._post_write_hook is not None:
            shc.async_create_task(
                self._post_write_hook(_ACTION_CREATE_UPDATE, config_key)
            )

        return self.json({"result": "ok"})

    async def delete(self, request, config_key):
        """Remove an entry."""
        shc = request.app[core.Const.KEY_SHC]
        async with self._mutation_lock:
            current = await self.read_config(shc)
            value = self._get_value(shc, current, config_key)
            path = shc.config.path(self._path)

            if value is None:
                return self.json_message(
                    "Resource not found", http.HTTPStatus.BAD_REQUEST
                )

            self._delete_value(shc, current, config_key)
            await shc.async_add_executor_job(_write, path, current)

        if self._post_write_hook is not None:
            shc.async_create_task(self._post_write_hook(_ACTION_DELETE, config_key))

        return self.json({"result": "ok"})

    async def read_config(self, shc: core.SmartHomeController) -> core.JsonType:
        """Read the config."""
        current = await shc.async_add_executor_job(_read, shc.config.path(self._path))
        if not current:
            current = self._empty_config()
        return current


def _read(path: pathlib.Path) -> core.JsonType:
    """Read YAML helper."""
    if not os.path.isfile(path):
        return None

    return core.YamlLoader.load_yaml(path)


def _write(path: pathlib.Path, data: core.JsonType):
    """Write YAML helper."""
    # Do it before opening file. If dump causes error it will now not
    # truncate the file.
    contents = core.helpers.dump(data)
    core.helpers.write_utf8_file_atomic(path, contents)
