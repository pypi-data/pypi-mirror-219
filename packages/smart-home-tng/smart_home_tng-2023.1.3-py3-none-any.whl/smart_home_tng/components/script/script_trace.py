"""
Scene Component for Smart Home - The Next Generation.

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

import contextlib
import typing

from ... import core


# pylint: disable=unused-variable
class ScriptTrace(core.ActionTrace):
    """Container for script trace."""

    def __init__(
        self,
        domain: str,
        item_id: str,
        config: dict[str, typing.Any],
        blueprint_inputs: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        super().__init__(domain, item_id, config, blueprint_inputs, context)

    @staticmethod
    @contextlib.contextmanager
    def trace_script(
        owner: core.ScriptComponent,
        item_id: str,
        config: dict[str, typing.Any],
        blueprint_inputs: dict[str, typing.Any],
        context: core.Context,
        trace_config: dict[str, typing.Any],
    ) -> typing.Iterator:
        """Trace execution of a script."""
        trace = ScriptTrace(owner.domain, item_id, config, blueprint_inputs, context)
        comp = owner.get_component(core.Const.TRACE_COMPONENT_NAME)
        if isinstance(comp, core.TraceComponent):
            comp.store_trace(trace, trace_config[core.Const.CONF_STORED_TRACES])

        try:
            yield trace
        except Exception as ex:
            if item_id:
                trace.set_error(ex)
            raise ex
        finally:
            if item_id:
                trace.finished()
