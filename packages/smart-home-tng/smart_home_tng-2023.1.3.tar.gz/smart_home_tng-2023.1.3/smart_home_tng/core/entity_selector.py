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

import typing

import voluptuous as vol

from .config_validation import ConfigValidation as cv
from .entity_selector_config import EntitySelectorConfig
from .selector import Selector
from .single_entity_selector_config import SINGLE_ENTITY_SELECTOR_CONFIG_SCHEMA


# pylint: disable=unused-variable
class EntitySelector(Selector):
    """Selector of a single or list of entities."""

    _CONFIG_SCHEMA: typing.Final = SINGLE_ENTITY_SELECTOR_CONFIG_SCHEMA.extend(
        {
            vol.Optional("exclude_entities"): [str],
            vol.Optional("include_entities"): [str],
            vol.Optional("multiple", default=False): cv.boolean,
        }
    )

    def config_schema(self, config: typing.Any) -> typing.Callable:
        return EntitySelector._CONFIG_SCHEMA(config)

    def __init__(self, config: EntitySelectorConfig = None) -> None:
        """Instantiate a selector."""
        super().__init__("entity", config)

    def __call__(self, data: typing.Any) -> str | list[str]:
        """Validate the passed selection."""

        include_entities = self._config.get("include_entities")
        exclude_entities = self._config.get("exclude_entities")

        def validate(e_or_u: str) -> str:
            e_or_u = cv.entity_id_or_uuid(e_or_u)
            if not cv.valid_entity_id(e_or_u):
                return e_or_u
            if allowed_domains := cv.ensure_list(self._config.get("domain")):
                domain = cv.split_entity_id(e_or_u)[0]
                if domain not in allowed_domains:
                    raise vol.Invalid(
                        f"Entity {e_or_u} belongs to domain {domain}, "
                        f"expected {allowed_domains}"
                    )
            if include_entities:
                vol.In(include_entities)(e_or_u)
            if exclude_entities:
                vol.NotIn(exclude_entities)(e_or_u)
            return e_or_u

        if not self._config["multiple"]:
            return validate(data)
        if not isinstance(data, list):
            raise vol.Invalid("Value should be a list")
        return typing.cast(list, vol.Schema([validate])(data))  # Output is a list
