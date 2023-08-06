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

import asyncio
import logging
import typing

from ... import core

if not typing.TYPE_CHECKING:

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .pyscript_component import PyscriptComponent

_LOGGER: typing.Final = logging.getLogger(__package__ + ".event")


# pylint: disable=unused-variable
class Events:
    """Define event functions."""

    def __init__(self, owner: PyscriptComponent):
        self._owner = owner

        #
        # notify message queues by event type
        #
        self._notify: dict[str, set[asyncio.Queue]] = {}
        self._notify_remove: dict[str, core.CallbackType] = {}

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @property
    def pyscript(self) -> PyscriptComponent:
        return self._owner

    async def event_listener(self, event: core.Event):
        """Listen callback for given event which updates any notifications."""

        func_args = {
            "trigger_type": "event",
            "event_type": event.event_type,
            "context": event.context,
        }
        func_args.update(event.data)
        await self.update(event.event_type, func_args)

    def notify_add(self, event_type: str, queue: asyncio.Queue):
        """Register to notify for events of given type to be sent to queue."""

        if event_type not in self._notify:
            self._notify[event_type] = set()
            _LOGGER.debug(f"event.notify_add({event_type}) -> adding event listener")
            self._notify_remove[event_type] = self.controller.bus.async_listen(
                event_type, self.event_listener
            )
        self._notify[event_type].add(queue)

    def notify_del(self, event_type: str, queue: asyncio.Queue):
        """Unregister to notify for events of given type for given queue."""

        registered = self._notify.get(event_type)
        if registered:
            registered.discard(queue)
            if len(registered) == 0:
                self._notify_remove[event_type]()
                _LOGGER.debug(
                    f"event.notify_del({event_type}) -> removing event listener",
                    event_type,
                )
                del self._notify[event_type]
                del self._notify_remove[event_type]

    async def update(self, event_type: str, func_args: dict[str, typing.Any]):
        """Deliver all notifications for an event of the given type."""

        _LOGGER.debug(
            f"event.update({event_type}, {vars}, {func_args})",
            event_type,
            vars,
            func_args,
        )
        queues = self._notify.get(event_type)
        if queues:
            for queue in queues:
                await queue.put(["event", func_args])
