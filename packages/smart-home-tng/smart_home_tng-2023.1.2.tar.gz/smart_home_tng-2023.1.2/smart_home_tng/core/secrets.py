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
import pathlib
import typing

from .const import Const
from .smart_home_controller_error import SmartHomeControllerError
from .yaml_loader import YamlLoader

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class Secrets:
    """Store secrets while loading YAML."""

    def __init__(self, config_dir: pathlib.Path) -> None:
        """Initialize secrets."""
        self.config_dir = config_dir
        self._cache: dict[pathlib.Path, dict[str, str]] = {}

    def get(self, requester_path: str, secret: str) -> str:
        """Return the value of a secret."""
        current_path = pathlib.Path(requester_path)

        secret_dir = current_path
        while True:
            secret_dir = secret_dir.parent

            try:
                secret_dir.relative_to(self.config_dir)
            except ValueError:
                # We went above the config dir
                break

            secrets = self._load_secret_yaml(secret_dir)

            if secret in secrets:
                _LOGGER.debug(
                    f"Secret {secret} retrieved from secrets.yaml in folder {secret_dir}"
                )
                return secrets[secret]

        raise SmartHomeControllerError(f"Secret {secret} not defined")

    def _load_secret_yaml(self, secret_dir: pathlib.Path) -> dict[str, str]:
        """Load the secrets yaml from path."""
        secret_path = pathlib.Path(secret_dir, Const.SECRET_YAML)
        if secret_path in self._cache:
            return self._cache[secret_path]

        _LOGGER.debug(f"Loading {secret_path}")
        try:
            secrets = YamlLoader.load_yaml(str(secret_path))

            if not isinstance(secrets, dict):
                raise SmartHomeControllerError("Secrets is not a dictionary")

            if "logger" in secrets:
                logger = str(secrets["logger"]).lower()
                if logger == "debug":
                    _LOGGER.setLevel(logging.DEBUG)
                else:
                    _LOGGER.error(
                        "Error in secrets.yaml: 'logger: debug' expected, "
                        + f"but 'logger: {logger}' found"
                    )
                del secrets["logger"]
        except FileNotFoundError:
            secrets = {}

        self._cache[secret_path] = secrets

        return secrets
