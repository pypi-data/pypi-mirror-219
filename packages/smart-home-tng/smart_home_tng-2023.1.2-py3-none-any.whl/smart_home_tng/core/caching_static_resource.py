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

import pathlib

from aiohttp import web

from .const import Const


# pylint: disable=unused-variable
class CachingStaticResource(web.StaticResource):
    """Static Resource handler that will add cache headers."""

    async def _handle(self, request: web.Request) -> web.StreamResponse:
        rel_url = request.match_info["filename"]
        try:
            filename = pathlib.Path(rel_url)
            if filename.anchor:
                # rel_url is an absolute name like
                # /static/\\machine_name\c$ or /static/D:\path
                # where the static dir is totally different
                raise web.HTTPForbidden()
            filepath = self._directory.joinpath(filename).resolve()
            if not self._follow_symlinks:
                filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError) as error:
            # relatively safe
            raise web.HTTPNotFound() from error
        except Exception as error:
            # perm error or other kind!
            request.app.logger.exception(error)
            raise web.HTTPNotFound() from error

        # on opening a dir, load its contents if allowed
        if filepath.is_dir():
            return await super()._handle(request)
        if filepath.is_file():
            return web.FileResponse(
                filepath,
                chunk_size=self._chunk_size,
                headers=Const.CACHE_HEADERS,
            )
        raise web.HTTPNotFound
