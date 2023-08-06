"""
PyScript Component for Smart Home - The Next Generation.

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


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import typing

_UNDEFINED: typing.Final = object()


# pylint: disable=unused-variable
class EvalLocalVar:
    """Wrapper for local variable symtable entry."""

    def __init__(self, name: str, **kwargs):
        """Initialize value of local symbol."""
        self._name = name
        self._defined = False
        self._value = None
        value = kwargs.get("value")
        if value is not _UNDEFINED:
            self._value = value
            self._defined = True

    @property
    def name(self) -> str:
        return self._name

    def get(self):
        """Get value of local symbol."""
        if not self._defined:
            raise NameError(f"name '{self.name}' is not defined")
        return self._value

    def set(self, value: typing.Any):
        """Set value of local symbol."""
        self._value = value
        self._defined = True

    @property
    def is_defined(self):
        """Return whether value is defined."""
        return self._defined

    def set_undefined(self):
        """Set local symbol to undefined."""
        self._defined = False

    def __getattr__(self, attr: str):
        """Get attribute of local variable."""
        if not self._defined:
            raise NameError(f"name '{self.name}' is not defined")
        return getattr(self._value, attr)

    def __repr__(self):
        """Generate string with address and value."""
        return f"EvalLocalVar @{hex(id(self))} = {self._value if self._defined else 'undefined'}"
