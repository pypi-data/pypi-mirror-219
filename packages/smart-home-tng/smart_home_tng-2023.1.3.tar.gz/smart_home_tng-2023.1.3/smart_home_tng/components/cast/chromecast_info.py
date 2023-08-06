"""
Google Cast Integration for Smart Home - The Next Generation.

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

import attr
import pychromecast as google

from .chromecast_zeroconf import ChromecastZeroconf

if not typing.TYPE_CHECKING:

    class GoogleCastIntegration:
        pass


if typing.TYPE_CHECKING:
    from .google_cast_integration import GoogleCastIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
@attr.s(slots=True, frozen=True)
class ChromecastInfo:
    """Class to hold all data about a chromecast for creating connections.

    This also has the same attributes as the mDNS fields by zeroconf.
    """

    cast_info: google.CastInfo = attr.ib()
    is_dynamic_group = attr.ib(type=typing.Optional[bool], default=None)

    @property
    def friendly_name(self) -> str:
        """Return the Friendly Name."""
        return self.cast_info.friendly_name

    @property
    def is_audio_group(self) -> bool:
        """Return if the cast is an audio group."""
        return self.cast_info.cast_type == google.const.CAST_TYPE_GROUP

    @property
    def uuid(self) -> str:
        """Return the UUID."""
        return self.cast_info.uuid

    def fill_out_missing_chromecast_info(self, owner: GoogleCastIntegration):
        """Return a new ChromecastInfo object with missing attributes filled in.

        Uses blocking HTTP / HTTPS.
        """
        cast_info = self.cast_info
        if self.cast_info.cast_type is None or self.cast_info.manufacturer is None:
            unknown_models = owner.unknown_models
            if self.cast_info.model_name not in unknown_models:
                # Manufacturer and cast type is not available in mDNS data, get it over http
                cast_info = google.dial.get_cast_type(
                    cast_info,
                    zconf=ChromecastZeroconf.get_zeroconf(),
                )
                unknown_models[self.cast_info.model_name] = (
                    cast_info.cast_type,
                    cast_info.manufacturer,
                )

                report_issue = (
                    "create a bug report at "
                    + "https://github.com/home-assistant/core/issues?q=is%3Aopen+is%3Aissue"
                    + "+label%3A%22integration%3A+cast%22"
                )

                _LOGGER.info(
                    f"Fetched cast details for unknown model '{cast_info.model_name}' "
                    + f"manufacturer: '{cast_info.manufacturer}', "
                    + f"type: '{cast_info.cast_type}'. Please {report_issue}",
                )
            else:
                cast_type, manufacturer = unknown_models[self.cast_info.model_name]
                cast_info = google.CastInfo(
                    cast_info.services,
                    cast_info.uuid,
                    cast_info.model_name,
                    cast_info.friendly_name,
                    cast_info.host,
                    cast_info.port,
                    cast_type,
                    manufacturer,
                )

        if not self.is_audio_group or self.is_dynamic_group is not None:
            # We have all information, no need to check HTTP API.
            return ChromecastInfo(cast_info=cast_info)

        # Fill out missing group information via HTTP API.
        is_dynamic_group = False
        http_group_status = None
        http_group_status = google.dial.get_multizone_status(
            None,
            services=self.cast_info.services,
            zconf=ChromecastZeroconf.get_zeroconf(),
        )
        if http_group_status is not None:
            is_dynamic_group = any(
                g.uuid == self.cast_info.uuid for g in http_group_status.dynamic_groups
            )

        return ChromecastInfo(
            cast_info=cast_info,
            is_dynamic_group=is_dynamic_group,
        )
