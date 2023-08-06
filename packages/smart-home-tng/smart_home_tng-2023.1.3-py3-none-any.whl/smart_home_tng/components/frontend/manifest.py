"""
Frontend Component for Smart Home - The Next Generation.

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

import json
import typing


# pylint: disable=unused-variable
class _Manifest:
    """Manage the manifest.json contents."""

    def __init__(self, data: dict) -> None:
        """Init the manifest manager."""
        self.manifest = data
        self._serialize()

    def __getitem__(self, key: str) -> typing.Any:
        """Return an item in the manifest."""
        return self.manifest[key]

    @property
    def json(self) -> str:
        """Return the serialized manifest."""
        return self._serialized

    def _serialize(self) -> None:
        self._serialized = json.dumps(self.manifest, sort_keys=True)

    def update_key(self, key: str, val: str) -> None:
        """Add a keyval to the manifest.json."""
        self.manifest[key] = val
        self._serialize()
