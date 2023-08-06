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

import struct


# pylint: disable=unused-variable
class ZmqSocket:
    """Defines a minimal implementation of a small subset of ZMQ."""

    #
    # This allows pyscript to work with Jupyter without the real zmq
    # and pyzmq packages, which might not be available or easy to
    # install on the wide set of HASS platforms.
    #
    def __init__(self, reader, writer, sock_type: str):
        """Initialize a ZMQ socket with the given type and reader/writer streams."""
        self._writer = writer
        self._reader = reader
        self._type = sock_type

    async def read_bytes(self, num_bytes):
        """Read bytes from ZMQ socket."""
        data = b""
        while len(data) < num_bytes:
            new_data = await self._reader.read(num_bytes - len(data))
            if len(new_data) == 0:
                raise EOFError
            data += new_data
        return data

    async def write_bytes(self, raw_msg):
        """Write bytes to ZMQ socket."""
        self._writer.write(raw_msg)
        await self._writer.drain()

    async def handshake(self):
        """Do initial greeting handshake on a new ZMQ connection."""
        await self.write_bytes(b"\xff\x00\x00\x00\x00\x00\x00\x00\x01\x7f")
        _ = await self.read_bytes(10)
        # _LOGGER.debug(f"handshake: got initial greeting {greeting}")
        await self.write_bytes(b"\x03")
        _ = await self.read_bytes(1)
        await self.write_bytes(
            b"\x00" + b"NULL" + b"\x00" * 16 + b"\x00" + b"\x00" * 31
        )
        _ = await self.read_bytes(53)
        # _LOGGER.debug(f"handshake: got rest of greeting {greeting}")
        params = [["Socket-Type", self._type]]
        if self._type == "ROUTER":
            params.append(["Identity", ""])
        await self.send_cmd("READY", params)

    async def recv(self, multipart=False):
        """Receive a message from ZMQ socket."""
        parts = []
        while 1:
            cmd = (await self.read_bytes(1))[0]
            if cmd & 0x2:
                msg_len = struct.unpack(">Q", await self.read_bytes(8))[0]
            else:
                msg_len = (await self.read_bytes(1))[0]
            msg_body = await self.read_bytes(msg_len)
            if cmd & 0x4:
                # _LOGGER.debug(f"recv: got cmd {msg_body}")
                cmd_len = msg_body[0]
                cmd = msg_body[1 : cmd_len + 1]
                msg_body = msg_body[cmd_len + 1 :]
                params = []
                while len(msg_body) > 0:
                    param_len = msg_body[0]
                    param = msg_body[1 : param_len + 1]
                    msg_body = msg_body[param_len + 1 :]
                    value_len = struct.unpack(">L", msg_body[0:4])[0]
                    value = msg_body[4 : 4 + value_len]
                    msg_body = msg_body[4 + value_len :]
                    params.append([param, value])
                # _LOGGER.debug(f"recv: got cmd={cmd}, params={params}")
            else:
                parts.append(msg_body)
                if cmd in (0x0, 0x2):
                    # _LOGGER.debug(f"recv: got msg {parts}")
                    if not multipart:
                        return b"".join(parts)

                    return parts

    async def recv_multipart(self):
        """Receive a multipart message from ZMQ socket."""
        return await self.recv(multipart=True)

    async def send_cmd(self, cmd, params):
        """Send a command over ZMQ socket."""
        raw_msg = bytearray([len(cmd)]) + cmd.encode()
        for param in params:
            raw_msg += bytearray([len(param[0])]) + param[0].encode()
            raw_msg += struct.pack(">L", len(param[1])) + param[1].encode()
        len_msg = len(raw_msg)
        if len_msg <= 255:
            raw_msg = bytearray([0x4, len_msg]) + raw_msg
        else:
            raw_msg = bytearray([0x6]) + struct.pack(">Q", len_msg) + raw_msg
        # _LOGGER.debug(f"send_cmd: sending {raw_msg}")
        await self.write_bytes(raw_msg)

    async def send(self, msg):
        """Send a message over ZMQ socket."""
        len_msg = len(msg)
        if len_msg <= 255:
            raw_msg = bytearray([0x1, 0x0, 0x0, len_msg]) + msg
        else:
            raw_msg = bytearray([0x1, 0x0, 0x2]) + struct.pack(">Q", len_msg) + msg
        # _LOGGER.debug(f"send: sending {raw_msg}")
        await self.write_bytes(raw_msg)

    async def send_multipart(self, parts):
        """Send multipart messages over ZMQ socket."""
        raw_msg = b""
        for i, part in enumerate(parts):
            len_part = len(part)
            cmd = 0x1 if i < len(parts) - 1 else 0x0
            if len_part <= 255:
                raw_msg += bytearray([cmd, len_part]) + part
            else:
                raw_msg += bytearray([cmd + 2]) + struct.pack(">Q", len_part) + part
        # _LOGGER.debug(f"send_multipart: sending {raw_msg}")
        await self.write_bytes(raw_msg)

    def close(self):
        """Close the ZMQ socket."""
        self._writer.close()
