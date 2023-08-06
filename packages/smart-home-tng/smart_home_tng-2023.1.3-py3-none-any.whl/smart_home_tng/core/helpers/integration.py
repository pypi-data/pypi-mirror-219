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

import asyncio
import collections.abc
import functools
import logging
import traceback
import typing

from ..missing_integration_frame import MissingIntegrationFrame

# Keep track of integrations already reported to prevent flooding
_REPORTED_INTEGRATIONS: set[str] = set()

_CallableT = typing.TypeVar("_CallableT", bound=collections.abc.Callable)
_LOGGER: typing.Final = logging.getLogger(__name__)


def get_integration_frame(
    exclude_integrations: set = None,
) -> tuple[traceback.FrameSummary, str, str]:
    """Return the frame, integration and integration path of the current stack frame."""
    found_frame = None
    if not exclude_integrations:
        exclude_integrations = set()

    for frame in reversed(traceback.extract_stack()):
        for path in ("custom_components/", "smart_home_tng/components/"):
            try:
                index = frame.filename.index(path)
                start = index + len(path)
                end = frame.filename.index("/", start)
                integration = frame.filename[start:end]
                if integration not in exclude_integrations:
                    found_frame = frame

                break
            except ValueError:
                continue

        if found_frame is not None:
            break

    if found_frame is None:
        raise MissingIntegrationFrame

    return found_frame, integration, path


def report(
    what: str,
    exclude_integrations: set = None,
    error_if_core: bool = True,
    level: int = logging.WARNING,
) -> None:
    """Report incorrect usage.

    Async friendly.
    """
    try:
        integration_frame = get_integration_frame(
            exclude_integrations=exclude_integrations
        )
    except MissingIntegrationFrame as err:
        msg = f"Detected code that {what}. Please report this issue."
        if error_if_core:
            raise RuntimeError(msg) from err
        _LOGGER.warning(msg, stack_info=True)
        return

    report_integration(what, integration_frame, level)


def report_integration(
    what: str,
    integration_frame: tuple[traceback.FrameSummary, str, str],
    level: int = logging.WARNING,
) -> None:
    """Report incorrect usage in an integration.

    Async friendly.
    """
    found_frame, integration, path = integration_frame

    # Keep track of integrations already reported to prevent flooding
    key = f"{found_frame.filename}:{found_frame.lineno}"
    if key in _REPORTED_INTEGRATIONS:
        return
    _REPORTED_INTEGRATIONS.add(key)

    index = found_frame.filename.index(path)
    if path == "custom_components/":
        extra = " to the custom component author"
    else:
        extra = ""

    _LOGGER.log(
        level,
        f"Detected integration that {what}. "
        + f"Please report issue{extra} for {integration} using this method at "
        + f"{found_frame.filename[index:]}, line {found_frame.lineno}: "
        + f"{(found_frame.line or '?').strip()}",
    )


# pylint: disable=unused-variable
def warn_use(func: _CallableT, what: str) -> _CallableT:
    """Mock a function to warn when it was about to be used."""
    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def report_use(*_args: typing.Any, **_kwargs: typing.Any) -> None:
            report(what)

    else:

        @functools.wraps(func)
        def report_use(*_args: typing.Any, **_kwargs: typing.Any) -> None:
            report(what)

    return typing.cast(_CallableT, report_use)
