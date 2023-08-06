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


# pylint: disable=unused-variable
class SourceFile:
    """Class for information about a source file."""

    def __init__(
        self,
        global_ctx_name: str = None,
        file_path: str = None,
        rel_path: str = None,
        rel_import_path: str = None,
        fq_mod_name: str = None,
        check_config: bool = None,
        app_config: dict = None,
        source: str = None,
        mtime: float = None,
        autoload: bool = None,
    ):
        self.global_ctx_name = global_ctx_name
        self.file_path = file_path
        self.rel_path = rel_path
        self.rel_import_path = rel_import_path
        self.fq_mod_name = fq_mod_name
        self.check_config = check_config
        self.app_config = app_config
        self.source = source
        self.mtime = mtime
        self.autoload = autoload
        self.force = False
