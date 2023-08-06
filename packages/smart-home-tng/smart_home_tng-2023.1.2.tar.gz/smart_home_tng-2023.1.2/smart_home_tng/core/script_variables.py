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

import collections.abc
import typing

from .callback import callback
from .template import Template


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class ScriptVariables:
    """Class to hold and render script variables."""

    def __init__(self, variables: dict[str, typing.Any]) -> None:
        """Initialize script variables."""
        self._variables = variables
        self._has_template: bool = None

    @property
    def variables(self) -> dict[str, typing.Any]:
        return self._variables

    @callback
    def async_render(
        self,
        shc: SmartHomeController,
        run_variables: collections.abc.Mapping[str, typing.Any],
        *,
        render_as_defaults: bool = True,
        limited: bool = False,
    ) -> dict[str, typing.Any]:
        """Render script variables.

        The run variables are used to compute the static variables.

        If `render_as_defaults` is True, the run variables will not be overridden.

        """
        if self._has_template is None:
            self._has_template = Template.is_complex(self._variables)
            Template.attach(shc, self._variables)

        if not self._has_template:
            if render_as_defaults:
                rendered_variables = dict(self._variables)

                if run_variables is not None:
                    rendered_variables.update(run_variables)
            else:
                rendered_variables = (
                    {} if run_variables is None else dict(run_variables)
                )
                rendered_variables.update(self._variables)

            return rendered_variables

        rendered_variables = {} if run_variables is None else dict(run_variables)

        for key, value in self._variables.items():
            # We can skip if we're going to override this key with
            # run variables anyway
            if render_as_defaults and key in rendered_variables:
                continue

            rendered_variables[key] = Template.render_complex(
                value, rendered_variables, limited
            )

        return rendered_variables

    def as_dict(self) -> dict[str, typing.Any]:
        """Return dict version of this class."""
        return self._variables
