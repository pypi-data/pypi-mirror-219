"""
Stream Component for Smart Home - The Next Generation.

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

from aiohttp import web

from ... import core
from .stream import Stream

if not typing.TYPE_CHECKING:

    class StreamComponent:
        pass


if typing.TYPE_CHECKING:
    from .stream_component import StreamComponent


# pylint: disable=unused-variable
class StreamView(core.SmartHomeControllerView):
    """
    Base StreamView.

    For implementation of a new stream format, define `url` and `name`
    attributes, and implement `handle` method in a child class.
    """

    def __init__(
        self,
        owner: StreamComponent,
        url: str = None,
        name: str = None,
        extra_urls: list[str] = None,
        cors_allowed=False,
    ):
        requires_auth = False
        super().__init__(url, name, extra_urls, requires_auth, cors_allowed)
        self._owner = owner
        self._platform = None

    async def get(
        self, request: web.Request, token: str, sequence: str = "", part_num: str = ""
    ) -> web.StreamResponse:
        """Start a GET request."""
        stream = next(
            (s for s in self._owner.streams if s.access_token == token),
            None,
        )

        if not stream:
            raise web.HTTPNotFound()

        # Start worker if not already started
        await stream.start()

        return await self.handle(request, stream, sequence, part_num)

    # pylint: disable=unused-argument
    async def handle(
        self, request: web.Request, stream: Stream, sequence: str, part_num: str
    ) -> web.StreamResponse:
        """Handle the stream request."""
        raise NotImplementedError()
