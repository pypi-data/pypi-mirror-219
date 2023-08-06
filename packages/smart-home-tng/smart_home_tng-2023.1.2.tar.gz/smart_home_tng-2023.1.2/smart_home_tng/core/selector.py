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

import abc
import typing

import voluptuous as vol
import yaml

from . import helpers
from .registry import Registry


# pylint: disable=unused-variable
class Selector:
    """Base class for selectors."""

    @abc.abstractmethod
    def config_schema(self, config: typing.Any) -> typing.Any:
        ...

    def __init__(self, selector_type: str, config: typing.Any = None) -> None:
        """Instantiate a selector."""
        # Selectors can be empty
        if config is None:
            config = {}

        self._config = self.config_schema(config)
        self._selector_type = selector_type

    def serialize(self) -> typing.Any:
        """Serialize Selector for voluptuous_serialize."""
        return {"selector": {self._selector_type: self._config}}

    @staticmethod
    def _get_selector_class(config: typing.Any):
        """Get selector class type."""
        if not isinstance(config, dict):
            raise vol.Invalid("Expected a dictionary")

        if len(config) != 1:
            raise vol.Invalid(
                f"Only one type can be specified. Found {', '.join(config)}"
            )

        selector_type: str = list(config)[0]

        if (selector_class := _SELECTORS.get(selector_type)) is None:
            raise vol.Invalid(f"Unknown selector type {selector_type} found")

        return selector_class

    @staticmethod
    def selector(config: typing.Any):
        """Instantiate a selector."""
        selector_class = Selector._get_selector_class(config)
        selector_type = list(config)[0]

        return selector_class(config[selector_type])

    @staticmethod
    def validate_selector(config: typing.Any) -> dict:
        """Validate a selector."""
        selector_class = Selector._get_selector_class(config)
        selector_type = list(config)[0]

        selector_config = config[selector_type]
        # Selectors can be empty
        if selector_config is None:
            return {selector_type: {}}

        selector = selector_class(selector_config)
        return {
            selector_type: typing.cast(dict, selector.config_schema(selector_config))
        }


yaml.SafeDumper.add_representer(
    Selector,
    lambda dumper, value: helpers.represent_odict(
        dumper, "tag:yaml.org,2002:map", value.serialize()
    ),
)

_SELECTORS: Registry[str, type[Selector]] = Registry()
