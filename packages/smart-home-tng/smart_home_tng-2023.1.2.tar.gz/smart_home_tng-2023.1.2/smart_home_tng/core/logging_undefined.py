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

import logging
import typing

import jinja2

from .template_context import template_context as context

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class LoggingUndefined(jinja2.Undefined):
    """Log on undefined variables."""

    def _log_message(self):
        template, action = context.get() or ("", "rendering or compiling")
        _LOGGER.warning(
            f"Template variable warning: {self._undefined_message} when {action} "
            + f"'{template}'"
        )

    def _fail_with_undefined_error(self, *args, **kwargs):
        try:
            return super()._fail_with_undefined_error(*args, **kwargs)
        except self._undefined_exception as ex:
            template, action = context.get() or ("", "rendering or compiling")
            _LOGGER.error(
                f"Template variable error: {self._undefined_message} when {action} "
                + f"'{template}'"
            )
            raise ex

    def __str__(self):
        """Log undefined __str___."""
        self._log_message()
        return super().__str__()

    def __iter__(self):
        """Log undefined __iter___."""
        self._log_message()
        return super().__iter__()

    def __bool__(self):
        """Log undefined __bool___."""
        self._log_message()
        return super().__bool__()
