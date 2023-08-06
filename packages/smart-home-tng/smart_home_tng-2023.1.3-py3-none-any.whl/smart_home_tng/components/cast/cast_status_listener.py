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

import pychromecast.controllers.media
import pychromecast.controllers.multizone
import pychromecast.controllers.receiver
import pychromecast.socket_client


# pylint: disable=unused-variable
class CastStatusListener(
    pychromecast.controllers.media.MediaStatusListener,
    pychromecast.controllers.multizone.MultiZoneManagerListener,
    pychromecast.controllers.receiver.CastStatusListener,
    pychromecast.socket_client.ConnectionStatusListener,
):
    """Helper class to handle pychromecast status callbacks.

    Necessary because a CastDevice entity or dynamic group can create a new
    socket client and therefore callbacks from multiple chromecast connections can
    potentially arrive. This class allows invalidating past chromecast objects.
    """

    # pylint: disable=protected-access
    def __init__(self, cast_device, chromecast, mz_mgr, mz_only=False):
        """Initialize the status listener."""
        self._cast_device = cast_device
        self._uuid = chromecast.uuid
        self._valid = True
        self._mz_mgr = mz_mgr

        if cast_device._cast_info.is_audio_group:
            self._mz_mgr.add_multizone(chromecast)
        if mz_only:
            return

        chromecast.register_status_listener(self)
        chromecast.socket_client.media_controller.register_status_listener(self)
        chromecast.register_connection_listener(self)
        if not cast_device._cast_info.is_audio_group:
            self._mz_mgr.register_listener(chromecast.uuid, self)

    def new_cast_status(self, status):
        """Handle reception of a new CastStatus."""
        if self._valid:
            self._cast_device.new_cast_status(status)

    def new_media_status(self, status):
        """Handle reception of a new MediaStatus."""
        if self._valid:
            self._cast_device.new_media_status(status)

    def load_media_failed(self, item, error_code):
        """Handle reception of a new MediaStatus."""
        if self._valid:
            self._cast_device.load_media_failed(item, error_code)

    def new_connection_status(self, status):
        """Handle reception of a new ConnectionStatus."""
        if self._valid:
            self._cast_device.new_connection_status(status)

    def added_to_multizone(self, group_uuid):
        """Handle the cast added to a group."""

    def removed_from_multizone(self, group_uuid):
        """Handle the cast removed from a group."""
        if self._valid:
            self._cast_device.multizone_new_media_status(group_uuid, None)

    def multizone_new_cast_status(self, group_uuid, cast_status):
        """Handle reception of a new CastStatus for a group."""

    def multizone_new_media_status(self, group_uuid, media_status):
        """Handle reception of a new MediaStatus for a group."""
        if self._valid:
            self._cast_device.multizone_new_media_status(group_uuid, media_status)

    def invalidate(self):
        """Invalidate this status listener.

        All following callbacks won't be forwarded.
        """
        # pylint: disable=protected-access
        if self._cast_device._cast_info.is_audio_group:
            self._mz_mgr.remove_multizone(self._uuid)
        else:
            self._mz_mgr.deregister_listener(self._uuid, self)
        self._valid = False
