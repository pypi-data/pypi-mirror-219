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
import json
import logging
import typing

from ... import core

if not typing.TYPE_CHECKING:

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .pyscript_component import PyscriptComponent


_LOGGER: typing.Final = logging.getLogger(__package__ + ".mqtt")


# pylint: disable=unused-variable
class MQTT:
    """Define mqtt functions."""

    def __init__(self, owner: PyscriptComponent):
        """Initialize Mqtt."""
        self._owner = owner
        self._notify: dict[str, set[asyncio.Queue]] = {}
        self._notify_remove: dict[str, typing.Callable[[], None]] = {}
        self._mqtt = None
        mqtt = owner.controller.components.mqtt
        if isinstance(mqtt, core.MQTT.Component):
            self._mqtt = mqtt

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @property
    def pyscript(self) -> PyscriptComponent:
        return self._owner

    def _mqtt_message_handler_maker(self, subscribed_topic: str):
        """Closure for mqtt_message_handler."""

        async def mqtt_message_handler(mqttmsg):
            """Listen for MQTT messages."""
            func_args = {
                "trigger_type": "mqtt",
                "topic": mqttmsg.topic,
                "payload": mqttmsg.payload,
                "qos": mqttmsg.qos,
            }

            try:
                func_args["payload_obj"] = json.loads(mqttmsg.payload)
            except ValueError:
                pass

            await self._update(subscribed_topic, func_args)

        return mqtt_message_handler

    async def notify_add(self, topic: str, queue: asyncio.Queue):
        """Register to notify for mqtt messages of given topic to be sent to queue."""

        if topic not in self._notify and self._mqtt:
            self._notify[topic] = set()
            _LOGGER.debug(
                f"mqtt.notify_add({topic}) -> adding mqtt subscription", topic
            )
            self._notify_remove[topic] = await self._mqtt.async_subscribe(
                topic, self._mqtt_message_handler_maker(topic), encoding="utf-8", qos=0
            )
        self._notify[topic].add(queue)

    def notify_del(self, topic: str, queue: asyncio.Queue):
        """Unregister to notify for mqtt messages of given topic for given queue."""

        queues = self._notify.get(topic, None)
        if not queues or queue not in queues:
            return
        queues.discard(queue)
        if len(queues) == 0:
            self._notify_remove[topic]()
            _LOGGER.debug(f"mqtt.notify_del({topic}) -> removing mqtt subscription")
            del self._notify[topic]
            del self._notify_remove[topic]

    async def _update(self, topic: str, func_args: dict):
        """Deliver all notifications for an mqtt message on the given topic."""

        _LOGGER.debug(f"mqtt.update({topic}, {vars}, {func_args})")
        queues = self._notify.get(topic, None)
        if queues:
            for queue in queues:
                await queue.put(["mqtt", func_args])
