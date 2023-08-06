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

import typing

from ... import core
from .alexa_client import AlexaClient
from .alexa_media_switch import AlexaMediaSwitch

if not typing.TYPE_CHECKING:

    class AlexaAccountInfo:
        pass


if typing.TYPE_CHECKING:
    from .alexa_account_info import AlexaAccountInfo


# pylint: disable=unused-variable
class ShuffleSwitch(AlexaMediaSwitch):
    """Representation of a Alexa Media Shuffle switch."""

    def __init__(self, owner: AlexaAccountInfo, client: AlexaClient):
        """Initialize the Alexa Switch."""
        # Class info
        super().__init__(owner, client, "shuffle", "shuffle", "shuffle")

    @property
    def icon(self):
        """Return the icon of the switch."""
        return super()._icon("mdi:shuffle", "mdi:shuffle-disabled")

    @property
    def entity_category(self):
        """Return the entity category of the switch."""
        return core.EntityCategory.CONFIG
