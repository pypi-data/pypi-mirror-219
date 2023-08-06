"""
Media Player Component for Smart Home - The Next Generation.

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

import http

from aiohttp import hdrs
from aiohttp import typedefs as web_typedefs
from aiohttp import web

from ... import core


# pylint: disable=unused-variable
class MediaPlayerImageView(core.SmartHomeControllerView):
    """Media player view to serve an image."""

    def __init__(self, component: core.EntityComponent) -> None:
        """Initialize a media player view."""
        requires_auth = False
        url = "/api/media_player_proxy/{entity_id}"
        name = "api:media_player:image"
        extra_urls = [
            url + "/browse_media/{media_content_type}/{media_content_id}",
        ]
        super().__init__(url, name, extra_urls, requires_auth)
        self._component = component

    async def get(
        self,
        request: web.Request,
        entity_id: str,
        media_content_type: str = None,
        media_content_id: str = None,
    ) -> web.Response:
        """Start a get request."""
        if (player := self._component.get_entity(entity_id)) is None:
            status = (
                http.HTTPStatus.NOT_FOUND
                if request[core.Const.KEY_AUTHENTICATED]
                else http.HTTPStatus.UNAUTHORIZED
            )
            return web.Response(status=status)

        assert isinstance(player, core.MediaPlayer.Entity)
        authenticated = (
            request[core.Const.KEY_AUTHENTICATED]
            or request.query.get("token") == player.access_token
        )

        if not authenticated:
            return web.Response(status=http.HTTPStatus.UNAUTHORIZED)

        if media_content_type and media_content_id:
            media_image_id = request.query.get("media_image_id")
            data, content_type = await player.async_get_browse_image(
                media_content_type, media_content_id, media_image_id
            )
        else:
            data, content_type = await player.async_get_media_image()

        if data is None:
            return web.Response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

        headers: web_typedefs.LooseHeaders = {hdrs.CACHE_CONTROL: "max-age=3600"}
        return web.Response(body=data, content_type=content_type, headers=headers)
