"""
Input Select Component for Smart Home - The Next Generation.

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

import logging
import typing

import voluptuous as vol

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)

# pylint: disable=unused-variable


def _remove_duplicates(options: list[str], name: str) -> list[str]:
    """Remove duplicated options."""
    unique_options = list(dict.fromkeys(options))
    # This check was added in 2022.3
    # Reject YAML configured input_select with duplicates from 2022.6
    if len(unique_options) != len(options):
        _LOGGER.warning(
            f"Input select '{name or '<unnamed>'}' with options {options} had duplicated "
            + "options, the duplicates have been removed",
        )
    return unique_options


def _cv_input_select(cfg: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """Configure validation helper for input select (voluptuous)."""
    options = cfg[Const.CONF_OPTIONS]
    initial = cfg.get(Const.CONF_INITIAL)
    if initial is not None and initial not in options:
        raise vol.Invalid(
            f"initial state {initial} is not part of the options: {','.join(options)}"
        )
    cfg[Const.CONF_OPTIONS] = _remove_duplicates(options, cfg.get(core.Const.CONF_NAME))
    return cfg
