"""
Helpers for Components of Smart Home - The Next Generation.

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

import getpass
import os
import platform
import typing

from ..const import Const

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from ..smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
async def async_get_system_info(shc: SmartHomeController) -> dict[str, typing.Any]:
    """Return info about the system."""
    info_object = {
        "installation_type": "Unknown",
        "version": Const.__version__,
        "dev": "dev" in Const.__version__,
        "virtualenv": shc.is_virtual_env(),
        "python_version": platform.python_version(),
        "docker": False,
        "arch": platform.machine(),
        "timezone": str(shc.config.time_zone),
        "os_name": platform.system(),
        "os_version": platform.release(),
    }

    try:
        info_object["user"] = getpass.getuser()
    except KeyError:
        info_object["user"] = None

    if platform.system() == "Darwin":
        info_object["os_version"] = platform.mac_ver()[0]
    elif platform.system() == "Linux":
        info_object["docker"] = os.path.isfile("/.dockerenv")

    # Determine installation type on current data
    if info_object["docker"]:
        if info_object["user"] == "root" and os.path.isfile("/OFFICIAL_IMAGE"):
            info_object[
                "installation_type"
            ] = "Smart Home - The Next Generation Container"
        else:
            info_object["installation_type"] = "Unsupported Third Party Container"

    elif shc.is_virtual_env():
        info_object["installation_type"] = "Smart Home - The Next Generation Core"

    return info_object
