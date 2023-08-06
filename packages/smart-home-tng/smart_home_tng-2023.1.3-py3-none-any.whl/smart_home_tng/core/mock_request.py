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

import http
import json
import typing
from urllib import parse

import multidict

from .mock_stream_reader import MockStreamReader


# pylint: disable=unused-variable
class MockRequest:
    """Mock an aiohttp request."""

    def __init__(
        self,
        content: bytes,
        mock_source: str,
        method: str = "GET",
        status: int = http.HTTPStatus.OK,
        headers: dict[str, str] = None,
        query_string: str = None,
        url: str = "",
    ) -> None:
        """Initialize a request."""
        self._method = method
        self._url = url
        self._status = status
        self._headers: multidict.CIMultiDict[str] = multidict.CIMultiDict(headers or {})
        self._query_string = query_string or ""
        self._content = content
        self._mock_source = mock_source

    @property
    def mock_source(self) -> str:
        return self._mock_source

    @property
    def method(self) -> str:
        return self._method

    @property
    def url(self) -> str:
        return self._url

    @property
    def status(self) -> int:
        return self._status

    @property
    def headers(self) -> multidict.CIMultiDict:
        return self._headers

    @property
    def query_string(self) -> str:
        return self._query_string

    @property
    def query(self) -> multidict.MultiDict[str]:
        """Return a dictionary with the query variables."""
        return multidict.MultiDict(
            parse.parse_qsl(self._query_string, keep_blank_values=True)
        )

    @property
    def _text(self) -> str:
        """Return the body as text."""
        return self._content.decode("utf-8")

    @property
    def content(self) -> MockStreamReader:
        """Return the body as text."""
        return MockStreamReader(self._content)

    async def json(self) -> typing.Any:
        """Return the body as JSON."""
        return json.loads(self._text)

    async def post(self) -> multidict.MultiDict[str]:
        """Return POST parameters."""
        return multidict.MultiDict(parse.parse_qsl(self._text, keep_blank_values=True))

    async def text(self) -> str:
        """Return the body as text."""
        return self._text
