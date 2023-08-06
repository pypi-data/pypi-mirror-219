"""
Smart Home - The Next Generation.

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

import argparse
import asyncio
import faulthandler
import logging
import os
import sys
import threading
import typing

from . import core, scripts
from .core.the_next_generation import TheNextGeneration
from .core.event_loop_policy import EventLoopPolicy
from .core.setup_manager import SetupManager

_FAULT_LOG_FILENAME: typing.Final = "smart_home_tng.log.fault"
_TASK_CANCELATION_TIMEOUT: typing.Final = 5
_LOGGER: typing.Final = logging.getLogger(__name__)


async def _setup_and_run(runtime_config: core.RuntimeConfig) -> int:
    """Set up Smart Home - The Next Generation and run."""
    shc = await TheNextGeneration.async_from_config(runtime_config)

    if shc is None:
        return 1

    # threading._shutdown can deadlock forever
    # pylint: disable=protected-access
    threading._shutdown = core.ThreadWithException.deadlock_safe_shutdown

    return await shc.async_run()


def _validate_os() -> None:
    """
    Validate that Smart Home - The Next Generation is running in a supported
    operating system.
    """
    if not sys.platform.startswith(("darwin", "linux")):
        print(
            "Smart Home - The Next Generation only supports Linux, "
            + "OSX and Windows using WSL"
        )
        sys.exit(1)


def _validate_python() -> None:
    """Validate that the right Python version is running."""
    if sys.version_info[:3] < core.Const.REQUIRED_PYTHON_VER:
        print(
            "Smart Home - The Next Generation requires at least Python "
            + f"{core.Const.REQUIRED_PYTHON_VER[0]}."
            + f"{core.Const.REQUIRED_PYTHON_VER[1]}."
            + f"{core.Const.REQUIRED_PYTHON_VER[2]}"
        )
        sys.exit(1)


def _get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = argparse.ArgumentParser(
        description="Smart Home - The Next Generation: Observe, Control, Automate.",
        epilog=f"If restart is requested, exits with code {core.Const.RESTART_EXIT_CODE}",
    )
    parser.add_argument("--version", action="version", version=core.Const.__version__)
    parser.add_argument(
        "-c",
        "--config",
        metavar="path_to_config_dir",
        default=SetupManager.get_default_config_dir(),
        help="Directory that contains the Smart Home - The Next Generation configuration",
    )
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="Start Smart Home - The Next Generation in safe mode",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Start Smart Home - The Next Generation in debug mode",
    )
    parser.add_argument(
        "--open-ui", action="store_true", help="Open the webinterface in a browser"
    )
    parser.add_argument(
        "--skip-pip",
        action="store_true",
        help="Skips pip install of required packages on startup",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging to file."
    )
    parser.add_argument(
        "--log-rotate-days",
        type=int,
        default=None,
        help="Enables daily log rotation and keeps up to the specified days",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Log file to write to.  If not set, CONFIG/smart_home_tng.log is used",
    )
    parser.add_argument(
        "--log-no-color", action="store_true", help="Disable color logs"
    )
    parser.add_argument(
        "--script", nargs=argparse.REMAINDER, help="Run one of the embedded scripts"
    )
    parser.add_argument(
        "--ignore-os-check",
        action="store_true",
        help="Skips validation of operating system",
    )

    arguments = parser.parse_args()

    return arguments


def _check_threads() -> None:
    """Check if there are any lingering threads."""
    try:
        nthreads = sum(
            thread.is_alive() and not thread.daemon for thread in threading.enumerate()
        )
        if nthreads > 1:
            sys.stderr.write(f"Found {nthreads} non-daemonic threads.\n")

    # Somehow we sometimes seem to trigger an assertion in the python threading
    # module. It seems we find threads that have no associated OS level thread
    # which are not marked as stopped at the python level.
    except AssertionError:
        sys.stderr.write("Failed to count non-daemonic threads.\n")


def _ensure_config_path(config_dir: str) -> None:
    """Validate the configuration directory."""
    lib_dir = os.path.join(config_dir, "deps")

    # Test if configuration directory exists
    if not os.path.isdir(config_dir):
        if os.path.isfile(config_dir):
            print(
                f"Fatal Error: Specified configuration directory {config_dir} "
                "does not exist"
            )
            sys.exit(1)

        try:
            os.mkdir(config_dir)
        except OSError:
            print(
                "Fatal Error: Unable to create default configuration "
                f"directory {config_dir}"
            )
            sys.exit(1)

    # Test if library directory exists
    if not os.path.isdir(lib_dir):
        try:
            os.mkdir(lib_dir)
        except OSError:
            print(f"Fatal Error: Unable to create library directory {lib_dir}")
            sys.exit(1)


def main() -> int:
    """Start Smart Home - The Next Generation."""
    _validate_python()

    args = _get_arguments()

    if not args.ignore_os_check:
        _validate_os()

    if args.script is not None:
        return scripts.run(args.script)

    config_dir = os.path.abspath(os.path.join(os.getcwd(), args.config))
    _ensure_config_path(config_dir)

    runtime_conf = core.RuntimeConfig(
        config_dir=config_dir,
        verbose=args.verbose,
        log_rotate_days=args.log_rotate_days,
        log_file=args.log_file,
        log_no_color=args.log_no_color,
        skip_pip=args.skip_pip,
        safe_mode=args.safe_mode,
        debug=args.debug,
        open_ui=args.open_ui,
    )

    fault_file_name = os.path.join(config_dir, _FAULT_LOG_FILENAME)
    with open(fault_file_name, mode="a", encoding="utf8") as fault_file:
        faulthandler.enable(fault_file)
        exit_code = _run(runtime_conf)
        faulthandler.disable()

    if os.path.getsize(fault_file_name) == 0:
        os.remove(fault_file_name)

    _check_threads()

    return exit_code


def _run(runtime_config: core.RuntimeConfig) -> int:
    """Run Home Assistant."""
    asyncio.set_event_loop_policy(EventLoopPolicy(runtime_config.debug))
    # Backport of cpython 3.9 asyncio.run with a _cancel_all_tasks that times out
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_setup_and_run(runtime_config))
    finally:
        try:
            _cancel_all_tasks_with_timeout(loop, _TASK_CANCELATION_TIMEOUT)
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
        finally:
            asyncio.set_event_loop(None)
            loop.close()


def _cancel_all_tasks_with_timeout(
    loop: asyncio.AbstractEventLoop, timeout: int
) -> None:
    """Adapted _cancel_all_tasks from python 3.9 with a timeout."""
    to_cancel = asyncio.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(asyncio.wait(to_cancel, timeout=timeout))

    for task in to_cancel:
        if task.cancelled():
            continue
        if not task.done():
            _LOGGER.warning(
                f"Task could not be canceled and was still running after shutdown: {task}"
            )
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )


if __name__ == "__main__":
    sys.exit(main())
