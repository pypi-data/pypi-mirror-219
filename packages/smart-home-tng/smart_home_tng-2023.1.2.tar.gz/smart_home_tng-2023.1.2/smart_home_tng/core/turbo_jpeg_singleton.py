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
import typing

try:
    import turbojpeg

    # pylint: disable=invalid-name
    TurboJPEG: typing.TypeAlias = turbojpeg.TurboJPEG
except ImportError:
    turbojpeg = None

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class TurboJPEGSingleton:
    """
    Load TurboJPEG only once.

    Ensures we do not log load failures each snapshot
    since camera image fetches happen every few
    seconds.
    """

    __instance = None

    @staticmethod
    def instance():
        """Singleton for TurboJPEG."""
        if TurboJPEGSingleton.__instance is None and turbojpeg is not None:
            TurboJPEGSingleton()
        return TurboJPEGSingleton.__instance

    def __init__(self) -> None:
        """Try to create TurboJPEG only once."""
        try:
            # TurboJPEG checks for libturbojpeg
            # when its created, but it imports
            # numpy which may or may not work so
            # we have to guard the import here.

            TurboJPEGSingleton.__instance = TurboJPEG()
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                "Error loading libturbojpeg; Cameras may impact HomeKit performance"
            )
            TurboJPEGSingleton.__instance = False
