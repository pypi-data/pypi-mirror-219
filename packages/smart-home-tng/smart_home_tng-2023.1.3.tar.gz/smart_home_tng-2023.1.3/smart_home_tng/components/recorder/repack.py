"""
Recorder Component for Smart Home - The Next Generation.

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

import sqlalchemy as sql

from .const import Const
from .model import _ALL_TABLES


if not typing.TYPE_CHECKING:

    class Recorder:
        pass


if typing.TYPE_CHECKING:
    from .recorder import Recorder

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
def repack_database(instance: Recorder) -> None:
    """Repack based on engine type."""
    assert instance.engine is not None
    dialect_name = instance.engine.dialect.name

    # Execute sqlite command to free up space on disk
    if dialect_name == Const.SupportedDialect.SQLITE:
        _LOGGER.debug("Vacuuming SQL DB to free space")
        with instance.engine.connect() as conn:
            conn.execute(sql.text("VACUUM"))
            conn.commit()
        return

    # Execute postgresql vacuum command to free up space on disk
    if dialect_name == Const.SupportedDialect.POSTGRESQL:
        _LOGGER.debug("Vacuuming SQL DB to free space")
        with instance.engine.connect().execution_options(
            isolation_level="AUTOCOMMIT"
        ) as conn:
            conn.execute(sql.text("VACUUM"))
            conn.commit()
        return

    # Optimize mysql / mariadb tables to free up space on disk
    if dialect_name == Const.SupportedDialect.MYSQL:
        _LOGGER.debug("Optimizing SQL DB to free space")
        with instance.engine.connect() as conn:
            conn.execute(sql.text(f"OPTIMIZE TABLE {','.join(_ALL_TABLES)}"))
            conn.commit()
        return
