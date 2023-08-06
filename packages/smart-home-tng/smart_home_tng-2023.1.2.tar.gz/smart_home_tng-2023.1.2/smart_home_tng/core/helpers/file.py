"""
Helpers for Components of Smart Home - The Next Generation.

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
import os
import tempfile
import typing

import atomicwrites

from ..write_error import WriteError

_LOGGER: typing.Final = logging.getLogger(__name__)

# pylint: disable=unused-variable


def write_utf8_file_atomic(
    filename: str,
    utf8_data: str,
    private: bool = False,
) -> None:
    """Write a file and rename it into place using atomicwrites.

    Writes all or nothing.

    This function uses fsync under the hood. It should
    only be used to write mission critical files as
    fsync can block for a few seconds or longer if the
    disk is busy.

    Using this function frequently will significantly
    negatively impact performance.
    """
    try:
        with atomicwrites.AtomicWriter(filename, overwrite=True).open() as fdesc:
            if not private:
                os.fchmod(fdesc.fileno(), 0o644)
            fdesc.write(utf8_data)
    except OSError as error:
        _LOGGER.exception(f"Saving file failed: {filename}")
        raise WriteError(error) from error


def write_utf8_file(
    filename: str,
    utf8_data: str,
    private: bool = False,
) -> None:
    """Write a file and rename it into place.

    Writes all or nothing.
    """

    tmp_filename = ""
    tmp_path = os.path.split(filename)[0]
    try:
        # Modern versions of Python tempfile create this file with mode 0o600
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=tmp_path, delete=False
        ) as fdesc:
            fdesc.write(utf8_data)
            tmp_filename = fdesc.name
            if not private:
                os.fchmod(fdesc.fileno(), 0o644)
        os.replace(tmp_filename, filename)
    except OSError as error:
        _LOGGER.exception(f"Saving file failed: {filename}")
        raise WriteError(error) from error
    finally:
        if os.path.exists(tmp_filename):
            try:
                os.remove(tmp_filename)
            except OSError as err:
                # If we are cleaning up then something else went wrong, so
                # we should suppress likely follow-on errors in the cleanup
                _LOGGER.error(
                    f"File replacement cleanup failed for {tmp_filename} while "
                    + f"saving {filename}: {err}"
                )
