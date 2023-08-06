"""
Philips Hue Integration for Smart Home - The Next Generation.

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

import aiohue

from .const import Const

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from .hue_bridge import HueBridge

_LOGGER: typing.Final = logging.getLogger(__name__)

# pylint: disable=unused-variable


async def _hue_activate_scene_v1(
    bridge: HueBridge,
    group_name: str,
    scene_name: str,
    transition: int | None = None,
    is_retry: bool = False,
) -> bool:
    """Service for V1 bridge to call directly into bridge to set scenes."""
    api: aiohue.HueBridgeV1 = bridge.api
    if api.scenes is None:
        _LOGGER.warning(f"Hub {api.host} does not support scenes")
        return False

    group = next(
        (group for group in api.groups.values() if group.name == group_name),
        None,
    )
    # Additional scene logic to handle duplicate scene names across groups
    scene = next(
        (
            scene
            for scene in api.scenes.values()
            if scene.name == scene_name
            and group is not None
            and sorted(scene.lights) == sorted(group.lights)
        ),
        None,
    )
    # If we can't find it, fetch latest info and try again
    if not is_retry and (group is None or scene is None):
        await bridge.async_request_call(api.groups.update)
        await bridge.async_request_call(api.scenes.update)
        return await _hue_activate_scene_v1(
            bridge, group_name, scene_name, transition, is_retry=True
        )

    if group is None or scene is None:
        _LOGGER.debug(
            f"Unable to find scene {scene_name} for group {group} on bridge "
            + f"{bridge.host}",
        )
        return False

    await bridge.async_request_call(
        group.set_action, scene=scene.id, transitiontime=transition
    )
    return True


async def _hue_activate_scene_v2(
    bridge: HueBridge,
    group_name: str,
    scene_name: str,
    transition: int | None = None,
    dynamic: bool = True,
) -> bool:
    """Service for V2 bridge to call scene by name."""
    _LOGGER.warning(
        f"Use of service_call '{Const.SERVICE_HUE_ACTIVATE_SCENE}' is deprecated and "
        + "will be removed in a future release. Please use scene entities instead",
    )
    api: aiohue.HueBridgeV2 = bridge.api
    for scene in api.scenes:
        if scene.metadata.name.lower() != scene_name.lower():
            continue
        group = api.scenes.get_group(scene.id)
        if group.metadata.name.lower() != group_name.lower():
            continue
        # found match!
        if transition:
            transition = transition * 1000  # transition is in ms
        await bridge.async_request_call(
            api.scenes.recall, scene.id, dynamic=dynamic, duration=transition
        )
        return True
    _LOGGER.debug(
        f"Unable to find scene {scene_name} for group {group_name} on bridge "
        + f"{bridge.host}",
    )
    return False
