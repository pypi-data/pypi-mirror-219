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
import collections
import collections.abc
import logging
import types
import typing

from ..reproduce_state_platform import ReproduceStatePlatform
from ..context import Context
from ..integration_not_found import IntegrationNotFound
from ..platform import Platform

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass

    class SmartHomeControllerComponent:
        pass

    class State:
        pass


if typing.TYPE_CHECKING:
    from ..smart_home_controller import SmartHomeController
    from ..smart_home_controller_component import SmartHomeControllerComponent
    from ..state import State

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable


async def async_reproduce_states(
    shc: SmartHomeController,
    states: State | typing.Iterable[State],
    *,
    context: Context = None,
    reproduce_options: dict[str, typing.Any] = None,
) -> None:
    """Reproduce a list of states on multiple domains."""
    if isinstance(states, State):
        states = [states]

    to_call: dict[str, list[State]] = collections.defaultdict(list)

    for state in states:
        to_call[state.domain].append(state)

    if to_call:
        # run all domains in parallel
        await asyncio.gather(
            *(
                _reproduce_worker(shc, domain, data, context, reproduce_options)
                for domain, data in to_call.items()
            )
        )


async def _reproduce_worker(
    shc: SmartHomeController,
    domain: str,
    states_by_domain: list[State],
    context: Context,
    options: dict[str, typing.Any],
) -> None:
    try:
        integration = await shc.setup.async_get_integration(domain)
    except IntegrationNotFound:
        _LOGGER.warning(f"Trying to reproduce state for unknown integration: {domain}")
        return

    comp = SmartHomeControllerComponent.get_component(domain)
    if isinstance(comp, SmartHomeControllerComponent):
        # New class based implementation
        platform = comp.get_platform(Platform.REPRODUCE_STATE)
        if not isinstance(platform, ReproduceStatePlatform):
            _LOGGER.warning(f"Integration {domain} does not support reproduce state")
            return
        await platform.async_reproduce_states(
            states_by_domain, context=context, reproduce_options=options
        )
        return

    # Legacy module base implementation
    try:
        platform: types.ModuleType = integration.get_platform("reproduce_state")
    except ImportError:
        _LOGGER.warning(f"Integration {domain} does not support reproduce state")
        return

    await platform.async_reproduce_states(
        shc, states_by_domain, context=context, reproduce_options=options
    )


async def async_reproduce_state(
    shc: SmartHomeController,
    states: State | typing.Iterable[State],
    *,
    context: Context | None = None,
    reproduce_options: dict[str, typing.Any] | None = None,
) -> None:
    """Reproduce a list of states on multiple domains."""
    if isinstance(states, State):
        states = [states]

    to_call: dict[str, list[State]] = collections.defaultdict(list)

    for state in states:
        to_call[state.domain].append(state)

    async def worker(domain: str, states_by_domain: list[State]) -> None:
        try:
            integration = await shc.setup.async_get_integration(domain)
        except IntegrationNotFound:
            _LOGGER.warning(
                f"Trying to reproduce state for unknown integration: {domain}"
            )
            return

        shc_comp = SmartHomeControllerComponent.get_component(domain)
        if shc_comp is not None:
            platform = shc_comp.get_platform(Platform.REPRODUCE_STATE)
            if isinstance(platform, ReproduceStatePlatform):
                await platform.async_reproduce_states(
                    states_by_domain,
                    context=context,
                    reproduce_options=reproduce_options,
                )
        else:
            try:
                platform: types.ModuleType = integration.get_platform("reproduce_state")
            except ImportError:
                _LOGGER.warning(
                    f"Integration {domain} does not support reproduce state"
                )
                return

            await platform.async_reproduce_states(
                shc,
                states_by_domain,
                context=context,
                reproduce_options=reproduce_options,
            )

    if to_call:
        # run all domains in parallel
        await asyncio.gather(
            *(worker(domain, data) for domain, data in to_call.items())
        )
