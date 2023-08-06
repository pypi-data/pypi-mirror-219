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
import threading
import traceback
import typing

import sqlalchemy.exc as sql_exc
import sqlalchemy.pool as sql_pool

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)

# For debugging the MutexPool
_DEBUG_MUTEX_POOL: typing.Final = True
_DEBUG_MUTEX_POOL_TRACE: typing.Final = False

_POOL_SIZE: typing.Final = 5

_ADVISE_MSG: typing.Final = (
    "Use homeassistant.components.recorder.get_instance(hass).async_add_executor_job()"
)


# pylint: disable=unused-variable
class RecorderPool(sql_pool.SingletonThreadPool, sql_pool.NullPool):
    """A hybrid of NullPool and SingletonThreadPool.

    When called from the creating thread or db executor acts like SingletonThreadPool
    When called from any other thread, acts like NullPool
    """

    def __init__(self, creator, *args: typing.Any, **kw: typing.Any) -> None:
        """Create the pool."""
        pool_size = _POOL_SIZE
        if "pool_size" in kw:
            pool_size = kw.pop("pool_size")
        super().__init__(creator, pool_size=pool_size, *args, **kw)

    @property
    def recorder_or_dbworker(self) -> bool:
        """Check if the thread is a recorder or dbworker thread."""
        thread_name = threading.current_thread().name
        return bool(
            thread_name == "Recorder" or thread_name.startswith(Const.DB_WORKER_PREFIX)
        )

    # Any can be switched out for ConnectionPoolEntry in the next version of sqlalchemy
    def _do_return_conn(self, conn: typing.Any) -> typing.Any:
        if self.recorder_or_dbworker:
            return super()._do_return_conn(conn)
        return conn.close()

    def shutdown(self) -> None:
        """Close the connection."""
        if (
            self.recorder_or_dbworker
            and self._conn
            and hasattr(self._conn, "current")
            and (conn := self._conn.current())
        ):
            conn.close()

    def dispose(self) -> None:
        """Dispose of the connection."""
        if self.recorder_or_dbworker:
            super().dispose()

    # Any can be switched out for ConnectionPoolEntry in the next version of sqlalchemy
    def _do_get(self) -> typing.Any:
        if self.recorder_or_dbworker:
            return super()._do_get()
        core.helpers.check_loop(
            self._do_get_db_connection_protected,
            strict=True,
            advise_msg=_ADVISE_MSG,
        )
        return self._do_get_db_connection_protected()

    def _do_get_db_connection_protected(self) -> typing.Any:
        core.helpers.report(
            "accesses the database without the database executor; "
            f"{_ADVISE_MSG} "
            "for faster database operations",
            exclude_integrations={"recorder"},
            error_if_core=False,
        )
        return super(  # pylint: disable=bad-super-call
            sql_pool.NullPool, self
        )._create_connection()


class MutexPool(sql_pool.StaticPool):
    """A pool which prevents concurrent accesses from multiple threads.

    This is used in tests to prevent unsafe concurrent accesses to in-memory SQLite
    databases.
    """

    _reference_counter = 0
    pool_lock: threading.RLock

    def _do_return_conn(self, conn: typing.Any) -> None:
        if _DEBUG_MUTEX_POOL_TRACE:
            trace = traceback.extract_stack()
            trace_msg = "\n" + "".join(traceback.format_list(trace[:-1]))
        else:
            trace_msg = ""

        super()._do_return_conn(conn)
        if _DEBUG_MUTEX_POOL:
            self._reference_counter -= 1
            _LOGGER.debug(
                f"{threading.current_thread().name} return conn ctr: "
                + f"{self._reference_counter}{trace_msg}",
            )
        MutexPool.pool_lock.release()

    def _do_get(self) -> typing.Any:
        if _DEBUG_MUTEX_POOL_TRACE:
            trace = traceback.extract_stack()
            trace_msg = "".join(traceback.format_list(trace[:-1]))
        else:
            trace_msg = ""

        if _DEBUG_MUTEX_POOL:
            _LOGGER.debug(f"{threading.current_thread().name} wait conn{trace_msg}")
        got_lock = MutexPool.pool_lock.acquire(timeout=1)
        if not got_lock:
            raise sql_exc.SQLAlchemyError
        conn = super()._do_get()
        if _DEBUG_MUTEX_POOL:
            self._reference_counter += 1
            _LOGGER.debug(
                f"{threading.current_thread().name} get conn: ctr: {self._reference_counter}",
            )
        return conn

    def _create_connection(self):
        raise NotImplementedError()
