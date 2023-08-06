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

import re
import typing


# pylint: disable=unused-variable
class Const:
    """Required onstants."""

    COMMENT_REQUIREMENTS: typing.Final = (
        "Adafruit_BBIO",
        "avea",  # depends on bluepy
        "avion",
        "beacontools",
        "beewi_smartclim",  # depends on bluepy
        "bluepy",
        "decora",
        "decora_wifi",
        "evdev",
        "face_recognition",
        "opencv-python-headless",
        "pybluez",
        "pycups",
        "PySwitchbot",
        "pySwitchmate",
        "python-eq3bt",
        "python-gammu",
        "python-lirc",
        "pyuserinput",
        "tensorflow",
        "tf-models-official",
    )

    COMMENT_REQUIREMENTS_NORMALIZED: typing.Final = {
        commented.lower().replace("_", "-") for commented in COMMENT_REQUIREMENTS
    }
    PACKAGE_REGEX: typing.Final = re.compile(r"^(?:--.+\s)?([-_\.\w\d]+).*==.+$")
