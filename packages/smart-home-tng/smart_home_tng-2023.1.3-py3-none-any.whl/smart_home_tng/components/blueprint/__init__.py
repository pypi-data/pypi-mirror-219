"""
Blueprint Integration for Smart Home - The Next Generation.

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

import typing

# pylint: disable=unused-variable

from . import helpers
from .blueprint import Blueprint
from .blueprint_exception import BlueprintException
from .blueprint_integration import BlueprintIntegration
from .blueprint_with_name_exception import BlueprintWithNameException
from .const import Const
from .domain_blueprints import DomainBlueprints
from .failed_to_load import FailedToLoad
from .file_already_exists import FileAlreadyExists
from .imported_blueprint import ImportedBlueprint
from .invalid_blueprint import InvalidBlueprint
from .invalid_blueprint_inputs import InvalidBlueprintInputs
from .missing_input import MissingInput
from .unsupported_url import UnsupportedUrl

_: typing.Final = BlueprintIntegration(__path__)
