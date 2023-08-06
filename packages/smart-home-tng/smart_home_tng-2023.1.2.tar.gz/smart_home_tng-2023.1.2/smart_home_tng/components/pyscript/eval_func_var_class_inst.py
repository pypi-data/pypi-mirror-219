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
import weakref

from .eval_func import EvalFunc
from .eval_func_var import EvalFuncVar

if not typing.TYPE_CHECKING:

    class AstEval:
        pass


if typing.TYPE_CHECKING:
    from .ast_eval import AstEval


# pylint: disable=unused-variable
class EvalFuncVarClassInst(EvalFuncVar):
    """Class for a callable pyscript class instance function."""

    def __init__(self, func: EvalFunc, ast_ctx: AstEval, class_inst_weak: weakref.ref):
        """Initialize instance with given EvalFunc function."""
        super().__init__(func)
        self._ast_ctx = ast_ctx
        self._class_inst_weak = class_inst_weak

    async def call(self, ast_ctx: AstEval, *args, **kwargs):
        """Call the EvalFunc function."""
        return await self._func.call(ast_ctx, self._class_inst_weak(), *args, **kwargs)
