"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import logging
import typing

import alexapy

_LOGGER: typing.Final = logging.getLogger(__name__)

if not typing.TYPE_CHECKING:

    class AlexaMediaIntegration:
        pass


if typing.TYPE_CHECKING:
    from .alexa_media_integration import AlexaMediaIntegration


# pylint: disable=unused-variable
class AlexaMedia:
    """Implementation of Alexa Media Base object."""

    def __init__(
        self, owner: AlexaMediaIntegration, device, login: alexapy.AlexaLogin
    ) -> None:
        # pylint: disable=unexpected-keyword-arg
        """Initialize the Alexa device."""

        # Class info
        self._login = login
        self._alexa_api = alexapy.AlexaAPI(device, login)
        self._account = alexapy.hide_email(login.email)
        self._email = login.email
        self._owner = owner

    @property
    def account(self) -> str:
        return self._account

    @property
    def email(self) -> str:
        return self._email

    def check_login_changes(self):
        """Update Login object if it has changed."""
        try:
            login = self._owner[self._email].login
        except (AttributeError, KeyError):
            return
        if self._alexa_api.update_login(login):
            _LOGGER.debug("Login object has changed; updating")
            self._login = login
            self._email = login.email
            self._account = alexapy.hide_email(login.email)
