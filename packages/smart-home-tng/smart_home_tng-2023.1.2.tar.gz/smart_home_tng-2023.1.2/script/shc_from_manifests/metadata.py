"""
Code Generator for Smart Home - The Next Generation.

Generates helper code from component manifests.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022, Andreas Nixdorf

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

import configparser
import typing

from smart_home_tng.core.const import Const

from .code_validator import CodeValidator
from .config import Config
from .integration import Integration

_NAME: typing.Final = "metadata"


# pylint: disable=unused-variable
class MetaDataValidator(CodeValidator):
    """Package metadata validation."""

    def __init__(self):
        super().__init__(_NAME)

    def validate(self, integrations: dict[str, Integration], config: Config) -> None:
        """Validate project metadata keys."""
        metadata_path = config.root / "setup.cfg"
        parser = configparser.ConfigParser()
        parser.read(metadata_path)

        try:
            if parser["metadata"]["version"] != Const.__version__:
                config.add_error(
                    "metadata",
                    f"'metadata.version' value does not match '{Const.__version__}'",
                )
        except KeyError:
            config.add_error("metadata", "No 'metadata.version' key found!")

        required_py_version = f">={'.'.join(map(str, Const.REQUIRED_PYTHON_VER))}"
        try:
            if parser["options"]["python_requires"] != required_py_version:
                config.add_error(
                    "metadata",
                    f"'options.python_requires' value doesn't match '{required_py_version}",
                )
        except KeyError:
            config.add_error("metadata", "No 'options.python_requires' key found!")
