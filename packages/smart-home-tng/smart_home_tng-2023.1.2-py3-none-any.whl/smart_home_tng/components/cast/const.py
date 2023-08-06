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

import typing


# pylint: disable=unused-variable
class Const:
    """Consts for Cast integration."""

    # Stores a threading.Lock that is held by the internal pychromecast discovery.
    INTERNAL_DISCOVERY_RUNNING_KEY: typing.Final = "cast.discovery_running"
    # Stores UUIDs of cast devices that were added as entities. Doesn't store
    # None UUIDs.
    ADDED_CAST_DEVICES_KEY: typing.Final = "cast.added_cast_devices"
    # Stores an audio group manager.
    CAST_MULTIZONE_MANAGER_KEY: typing.Final = "cast.multizone_manager"
    # Store a CastBrowser
    CAST_BROWSER_KEY: typing.Final = "cast.browser"

    # Dispatcher signal fired with a ChromecastInfo every time we discover a new
    # Chromecast or receive it through configuration
    SIGNAL_CAST_DISCOVERED: typing.Final = "cast.discovered"

    # Dispatcher signal fired with a ChromecastInfo every time a Chromecast is
    # removed
    SIGNAL_CAST_REMOVED: typing.Final = "cast.removed"

    # Dispatcher signal fired when a Chromecast should show a Home Assistant Cast view.
    SIGNAL_CAST_SHOW_VIEW: typing.Final = "cast.show_view"

    CONF_IGNORE_CEC: typing.Final = "ignore_cec"
    CONF_KNOWN_HOSTS: typing.Final = "known_hosts"
    CONF_UUID: typing.Final = "uuid"
