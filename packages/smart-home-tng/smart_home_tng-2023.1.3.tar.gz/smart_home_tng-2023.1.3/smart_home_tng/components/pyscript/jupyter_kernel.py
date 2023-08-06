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
import datetime as dt
import json
import logging
import typing
import hmac
import hashlib
import re
import traceback
import uuid

from ... import core
from .ast_eval import AstEval
from .kernel_buffering_handler import KernelBufferingHandler
from .zmq_socket import ZmqSocket

if not typing.TYPE_CHECKING:

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .pyscript_component import PyscriptComponent

_LOGGER: typing.Final = logging.getLogger(__name__)

# Globals:

_DELIM: typing.Final = b"<IDS|MSG>"


# pylint: disable=unused-variable
class JupyterKernel:
    """Define a Jupyter Kernel class."""

    def __init__(self, owner: PyscriptComponent, config: dict, ast_ctx: AstEval):
        """Initialize a Kernel object, one instance per session."""
        self._owner = owner
        self._config = config.copy()
        self._ast_ctx = ast_ctx

        self._secure_key = _str_to_bytes(config["key"])
        self._no_connect_timeout = config.get("no_connect_timeout", 30)
        self._signature_schemes = {"hmac-sha256": hashlib.sha256}
        self._auth = hmac.HMAC(
            self._secure_key,
            digestmod=self._signature_schemes[config["signature_scheme"]],
        )
        self._execution_count = 1
        self._engine_id = str(uuid.uuid4())

        self._heartbeat_server = None
        self._iopub_server = None
        self._control_server = None
        self._stdin_server = None
        self._shell_server = None

        self._heartbeat_port = None
        self._iopub_port = None
        self._control_port = None
        self._stdin_port = None
        self._shell_port = None
        # this should probably be a configuration parameter
        self._avail_port = 50321

        # there can be multiple iopub subscribers, with corresponding tasks
        self._iopub_socket = set()

        self._tasks = {}
        self._task_cnt = 0
        self._task_cnt_max = 0

        self._session_cleanup_callback: typing.Callable[[], None] = None

        self._housekeep_q = asyncio.Queue(0)

        self._parent_header = None

        #
        # we create a logging handler so that output from the log functions
        # gets delivered back to Jupyter as stdout
        #
        self._console = KernelBufferingHandler(self._housekeep_q)
        self._console.setLevel(logging.DEBUG)
        # set a format which is just the message
        formatter = logging.Formatter("%(message)s")
        self._console.setFormatter(formatter)

        # match alphanum or "." at end of line
        self._completion_re = re.compile(r".*?([\w.]*)$", re.DOTALL)

        # see if line ends in a ":", with optional whitespace and comment
        # note: this doesn't detect if we are inside a quoted string...
        self._colon_end_re = re.compile(r".*: *(#.*)?$")

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @property
    def pyscript(self) -> PyscriptComponent:
        return self._owner

    def msg_sign(self, msg_lst):
        """Sign a message with a secure signature."""
        auth_hmac = self._auth.copy()
        for msg in msg_lst:
            auth_hmac.update(msg)
        return _str_to_bytes(auth_hmac.hexdigest())

    def deserialize_wire_msg(self, wire_msg):
        """Split the routing prefix and message frames from a message on the wire."""
        delim_idx = wire_msg.index(_DELIM)
        identities = wire_msg[:delim_idx]
        m_signature = wire_msg[delim_idx + 1]
        msg_frames = wire_msg[delim_idx + 2 :]

        def decode(msg):
            return json.loads(msg.decode("utf-8"))

        msg = {}
        msg["header"] = decode(msg_frames[0])
        msg["parent_header"] = decode(msg_frames[1])
        msg["metadata"] = decode(msg_frames[2])
        msg["content"] = decode(msg_frames[3])
        check_sig = self.msg_sign(msg_frames)
        if check_sig != m_signature:
            _LOGGER.error(
                f"signature mismatch: check_sig={check_sig}, m_signature={m_signature}, "
                + f"wire_msg={wire_msg}",
            )
            raise ValueError("Signatures do not match")

        return identities, msg

    def new_header(self, msg_type):
        """Make a new header."""
        return {
            "date": dt.datetime.now().isoformat(),
            "msg_id": _msg_id(),
            "username": "kernel",
            "session": self._engine_id,
            "msg_type": msg_type,
            "version": "5.3",
        }

    async def send(
        self,
        stream,
        msg_type,
        content=None,
        parent_header=None,
        metadata=None,
        identities=None,
    ):
        """Send message to the Jupyter client."""
        header = self.new_header(msg_type)

        def encode(msg):
            return _str_to_bytes(json.dumps(msg))

        msg_lst = [
            encode(header),
            encode(parent_header if parent_header else {}),
            encode(metadata if metadata else {}),
            encode(content if content else {}),
        ]
        signature = self.msg_sign(msg_lst)
        parts = [_DELIM, signature, msg_lst[0], msg_lst[1], msg_lst[2], msg_lst[3]]
        if identities:
            parts = identities + parts
        if stream:
            # _LOGGER.debug("send %s: %s", msg_type, parts)
            for this_stream in stream if isinstance(stream, set) else {stream}:
                await this_stream.send_multipart(parts)

    async def shell_handler(self, shell_socket, wire_msg):
        """Handle shell messages."""

        identities, msg = self.deserialize_wire_msg(wire_msg)
        self._parent_header = msg["header"]

        content = {
            "execution_state": "busy",
        }
        await self.send(
            self._iopub_socket, "status", content, parent_header=msg["header"]
        )

        msg_type = msg["header"]["msg_type"]
        if msg_type == "execute_request":
            content = {
                "execution_count": self._execution_count,
                "code": msg["content"]["code"],
            }
            await self.send(
                self._iopub_socket,
                "execute_input",
                content,
                parent_header=msg["header"],
            )

            code = msg["content"]["code"]
            #
            # replace VSCode initialization code, which depend on iPython % extensions
            #
            if code.startswith("%config "):
                code = "None"
            if code.startswith("_rwho_ls = %who_ls"):
                code = "print([])"

            global_ctx = self._ast_ctx.global_ctx
            global_ctx.set_auto_start(False)
            self._ast_ctx.parse(code)
            exc = self._ast_ctx.exception_obj
            if exc is None:
                result = await self._ast_ctx.eval()
                exc = self._ast_ctx.exception
            await self.pyscript.functions.waiter_sync()
            global_ctx.set_auto_start(True)
            global_ctx.start()
            if exc:
                traceback_mesg = self._ast_ctx.exception_long.split("\n")

                metadata = {
                    "dependencies_met": True,
                    "engine": self._engine_id,
                    "status": "error",
                    "started": dt.datetime.now().isoformat(),
                }
                content = {
                    "execution_count": self._execution_count,
                    "status": "error",
                    "ename": type(exc).__name__,  # Exception name, as a string
                    "evalue": str(exc),  # Exception value, as a string
                    "traceback": traceback_mesg,
                }
                _LOGGER.debug(f"Executing '{code}' got exception: {content}")
                await self.send(
                    shell_socket,
                    "execute_reply",
                    content,
                    metadata=metadata,
                    parent_header=msg["header"],
                    identities=identities,
                )
                del content["execution_count"], content["status"]
                await self.send(
                    self._iopub_socket, "error", content, parent_header=msg["header"]
                )

                content = {
                    "execution_state": "idle",
                }
                await self.send(
                    self._iopub_socket, "status", content, parent_header=msg["header"]
                )
                if msg["content"].get("store_history", True):
                    self._execution_count += 1
                return

            # if True or isinstance(self.ast_ctx.ast, ast.Expr):
            _LOGGER.debug(f"Executing: '{code}' got result {result}")
            if result is not None:
                content = {
                    "execution_count": self._execution_count,
                    "data": {"text/plain": repr(result)},
                    "metadata": {},
                }
                await self.send(
                    self._iopub_socket,
                    "execute_result",
                    content,
                    parent_header=msg["header"],
                )

            metadata = {
                "dependencies_met": True,
                "engine": self._engine_id,
                "status": "ok",
                "started": dt.datetime.now().isoformat(),
            }
            content = {
                "status": "ok",
                "execution_count": self._execution_count,
                "user_variables": {},
                "payload": [],
                "user_expressions": {},
            }
            await self.send(
                shell_socket,
                "execute_reply",
                content,
                metadata=metadata,
                parent_header=msg["header"],
                identities=identities,
            )
            if msg["content"].get("store_history", True):
                self._execution_count += 1

            #
            # Make sure stdout gets sent before set report execution_state idle on iopub,
            # otherwise VSCode doesn't display stdout.  We do a handshake with the
            # housekeep task to ensure any queued messages get processed.
            #
            handshake_q = asyncio.Queue(0)
            await self._housekeep_q.put(["handshake", handshake_q, 0])
            await handshake_q.get()

        elif msg_type == "kernel_info_request":
            content = {
                "protocol_version": "5.3",
                "ipython_version": [1, 1, 0, ""],
                "language_version": [0, 0, 1],
                "language": "python",
                "implementation": "python",
                "implementation_version": "3.7",
                "language_info": {
                    "name": "python",
                    "version": "1.0",
                    "mimetype": "",
                    "file_extension": ".py",
                    "codemirror_mode": "",
                    "nbconvert_exporter": "",
                },
                "banner": "",
            }
            await self.send(
                shell_socket,
                "kernel_info_reply",
                content,
                parent_header=msg["header"],
                identities=identities,
            )

        elif msg_type == "complete_request":
            root = ""
            words = set()
            code = msg["content"]["code"]
            posn = msg["content"]["cursor_pos"]
            match = self._completion_re.match(code[0:posn].lower())
            if match:
                root = match[1].lower()
                words = self.pyscript.states.completions(root)
                words = words.union(
                    await self.pyscript.functions.service_completions(root)
                )
                words = words.union(
                    await self.pyscript.functions.func_completions(root)
                )
                words = words.union(self._ast_ctx.completions(root))
            content = {
                "status": "ok",
                "matches": sorted(list(words)),
                "cursor_start": msg["content"]["cursor_pos"] - len(root),
                "cursor_end": msg["content"]["cursor_pos"],
                "metadata": {},
            }
            await self.send(
                shell_socket,
                "complete_reply",
                content,
                parent_header=msg["header"],
                identities=identities,
            )

        elif msg_type == "is_complete_request":
            code = msg["content"]["code"]
            self._ast_ctx.parse(code)
            exc = self._ast_ctx.exception_obj

            # determine indent of last line
            indent = 0
            i = code.rfind("\n")
            if i >= 0:
                while i + 1 < len(code) and code[i + 1] == " ":
                    i += 1
                    indent += 1
            if exc is None:
                if indent == 0:
                    content = {
                        # One of 'complete', 'incomplete', 'invalid', 'unknown'
                        "status": "complete",
                        # If status is 'incomplete', indent should contain the characters to use
                        # to indent the next line. This is only a hint: frontends may ignore it
                        # and use their own autoindentation rules. For other statuses, this
                        # field does not exist.
                        # "indent": str,
                    }
                else:
                    content = {
                        "status": "incomplete",
                        "indent": " " * indent,
                    }
            else:
                #
                # if the syntax error is right at the end, then we label it incomplete,
                # otherwise it's invalid
                #
                if "EOF while" in str(exc) or "expected an indented block" in str(exc):
                    # if error is at ":" then increase indent
                    if hasattr(exc, "lineno"):
                        line = code.split("\n")[exc.lineno - 1]
                        if self.colon_end_re.match(line):
                            indent += 4
                    content = {
                        "status": "incomplete",
                        "indent": " " * indent,
                    }
                else:
                    content = {
                        "status": "invalid",
                    }
            # _LOGGER.debug(f"is_complete_request code={code}, exc={exc}, content={content}")
            await self.send(
                shell_socket,
                "is_complete_reply",
                content,
                parent_header=msg["header"],
                identities=identities,
            )

        elif msg_type == "comm_info_request":
            content = {"comms": {}}
            await self.send(
                shell_socket,
                "comm_info_reply",
                content,
                parent_header=msg["header"],
                identities=identities,
            )

        elif msg_type == "history_request":
            content = {"history": []}
            await self.send(
                shell_socket,
                "history_reply",
                content,
                parent_header=msg["header"],
                identities=identities,
            )

        else:
            _LOGGER.error(f"unknown msg_type: {msg_type}")

        content = {
            "execution_state": "idle",
        }
        await self.send(
            self._iopub_socket, "status", content, parent_header=msg["header"]
        )

    async def _control_listen(self, reader, writer):
        """Task that listens to control messages."""
        try:
            _LOGGER.debug("control_listen connected")
            await self._housekeep_q.put(["register", "control", asyncio.current_task()])
            control_socket = ZmqSocket(reader, writer, "ROUTER")
            await control_socket.handshake()
            while 1:
                wire_msg = await control_socket.recv_multipart()
                identities, msg = self.deserialize_wire_msg(wire_msg)
                if msg["header"]["msg_type"] == "shutdown_request":
                    content = {
                        "restart": False,
                    }
                    await self.send(
                        control_socket,
                        "shutdown_reply",
                        content,
                        parent_header=msg["header"],
                        identities=identities,
                    )
                    await self._housekeep_q.put(["shutdown"])
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except (EOFError, ConnectionResetError):
            _LOGGER.debug("control_listen got eof")
            await self._housekeep_q.put(
                ["unregister", "control", asyncio.current_task()]
            )
            control_socket.close()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error(f"control_listen exception {err}")
            await self._housekeep_q.put(["shutdown"])

    async def _stdin_listen(self, reader, writer):
        """Task that listens to stdin messages."""
        try:
            _LOGGER.debug("stdin_listen connected")
            await self._housekeep_q.put(["register", "stdin", asyncio.current_task()])
            stdin_socket = ZmqSocket(reader, writer, "ROUTER")
            await stdin_socket.handshake()
            while 1:
                _ = await stdin_socket.recv_multipart()
                # _LOGGER.debug("stdin_listen received %s", _)
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except (EOFError, ConnectionResetError):
            _LOGGER.debug("stdin_listen got eof")
            await self._housekeep_q.put(["unregister", "stdin", asyncio.current_task()])
            stdin_socket.close()
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error(f"stdin_listen exception {traceback.format_exc(-1)}")
            await self._housekeep_q.put(["shutdown"])

    async def _shell_listen(self, reader, writer):
        """Task that listens to shell messages."""
        try:
            _LOGGER.debug("shell_listen connected")
            await self._housekeep_q.put(["register", "shell", asyncio.current_task()])
            shell_socket = ZmqSocket(reader, writer, "ROUTER")
            await shell_socket.handshake()
            while 1:
                msg = await shell_socket.recv_multipart()
                await self.shell_handler(shell_socket, msg)
        except asyncio.CancelledError:
            shell_socket.close()
            raise
        except (EOFError, ConnectionResetError):
            _LOGGER.debug("shell_listen got eof")
            await self._housekeep_q.put(["unregister", "shell", asyncio.current_task()])
            shell_socket.close()
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error(f"shell_listen exception {traceback.format_exc(-1)}")
            await self._housekeep_q.put(["shutdown"])

    async def _heartbeat_listen(self, reader, writer):
        """Task that listens and responds to heart beat messages."""
        try:
            _LOGGER.debug("heartbeat_listen connected")
            await self._housekeep_q.put(
                ["register", "heartbeat", asyncio.current_task()]
            )
            heartbeat_socket = ZmqSocket(reader, writer, "REP")
            await heartbeat_socket.handshake()
            while 1:
                msg = await heartbeat_socket.recv()
                # _LOGGER.debug("heartbeat_listen: got %s", msg)
                await heartbeat_socket.send(msg)
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except (EOFError, ConnectionResetError):
            _LOGGER.debug("heartbeat_listen got eof")
            await self._housekeep_q.put(
                ["unregister", "heartbeat", asyncio.current_task()]
            )
            heartbeat_socket.close()
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error(f"heartbeat_listen exception: {traceback.format_exc(-1)}")
            await self._housekeep_q.put(["shutdown"])

    async def _iopub_listen(self, reader, writer):
        """Task that listens to iopub messages."""
        try:
            _LOGGER.debug("iopub_listen connected")
            await self._housekeep_q.put(["register", "iopub", asyncio.current_task()])
            iopub_socket = ZmqSocket(reader, writer, "PUB")
            await iopub_socket.handshake()
            self._iopub_socket.add(iopub_socket)
            while 1:
                _ = await iopub_socket.recv_multipart()
                # _LOGGER.debug("iopub received %s", _)
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except (EOFError, ConnectionResetError):
            await self._housekeep_q.put(["unregister", "iopub", asyncio.current_task()])
            iopub_socket.close()
            self._iopub_socket.discard(iopub_socket)
            _LOGGER.debug("iopub_listen got eof")
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error(f"iopub_listen exception {traceback.format_exc(-1)}")
            await self._housekeep_q.put(["shutdown"])

    async def _housekeep_run(self):
        """Housekeeping, including closing servers after startup, and doing orderly shutdown."""
        while True:
            try:
                msg = await self._housekeep_q.get()
                if msg[0] == "stdout":
                    content = {"name": "stdout", "text": msg[1] + "\n"}
                    if self._iopub_socket:
                        await self.send(
                            self._iopub_socket,
                            "stream",
                            content,
                            parent_header=self._parent_header,
                            identities=[b"stream.stdout"],
                        )
                elif msg[0] == "handshake":
                    await msg[1].put(msg[2])
                elif msg[0] == "register":
                    if msg[1] not in self._tasks:
                        self._tasks[msg[1]] = set()
                    self._tasks[msg[1]].add(msg[2])
                    self._task_cnt += 1
                    self._task_cnt_max = max(self._task_cnt_max, self._task_cnt)
                    #
                    # now a couple of things are connected, call the session_cleanup_callback
                    #
                    if self._task_cnt > 1 and self._session_cleanup_callback:
                        self._session_cleanup_callback()
                        self._session_cleanup_callback = None
                elif msg[0] == "unregister":
                    if msg[1] in self._tasks:
                        self._tasks[msg[1]].discard(msg[2])
                    self._task_cnt -= 1
                    #
                    # if there are no connection tasks left, then shutdown the kernel
                    #
                    if self._task_cnt == 0 and self._task_cnt_max >= 4:
                        asyncio.create_task(self.session_shutdown())
                        await asyncio.sleep(10000)
                elif msg[0] == "shutdown":
                    asyncio.create_task(self.session_shutdown())
                    await asyncio.sleep(10000)
            except asyncio.CancelledError:  # pylint: disable=try-except-raise
                raise
            except Exception:  # pylint: disable=broad-except
                _LOGGER.error(f"housekeep task exception: {traceback.format_exc(-1)}")

    async def _startup_timeout(self):
        """Shut down the session if nothing connects after 30 seconds."""
        await self._housekeep_q.put(
            ["register", "startup_timeout", asyncio.current_task()]
        )
        await asyncio.sleep(self._no_connect_timeout)
        if self._task_cnt_max <= 1:
            #
            # nothing started other than us, so shut down the session
            #
            _LOGGER.error(
                f"No connections to session {self._ast_ctx.global_ctx.name}; shutting down"
            )
            if self._session_cleanup_callback:
                self._session_cleanup_callback()
                self._session_cleanup_callback = None
            await self._housekeep_q.put(["shutdown"])
        await self._housekeep_q.put(
            ["unregister", "startup_timeout", asyncio.current_task()]
        )

    async def _start_one_server(self, callback):
        """Start a server by finding an available port."""
        first_port = self._avail_port
        for _ in range(2048):
            try:
                server = await asyncio.start_server(  # nosec
                    callback, "0.0.0.0", self._avail_port
                )
                return server, self._avail_port
            except OSError:
                self._avail_port += 1
        _LOGGER.error(
            f"unable to find an available port from {first_port} to {self._avail_port - 1}",
        )
        return None, None

    def get_ports(self):
        """Return a dict of the port numbers this kernel session is listening to."""
        return {
            "iopub_port": self._iopub_port,
            "hb_port": self._heartbeat_port,
            "control_port": self._control_port,
            "stdin_port": self._stdin_port,
            "shell_port": self._shell_port,
        }

    def set_session_cleanup_callback(self, callback: typing.Callable[[], None]):
        """Set a cleanup callback which is called right after the session has started."""
        self._session_cleanup_callback = callback

    async def session_start(self):
        """Start the kernel session."""
        self._ast_ctx.add_logger_handler(self._console)
        _LOGGER.info(f"Starting session {self._ast_ctx.global_ctx.name}")

        self._tasks["housekeep"] = {asyncio.create_task(self._housekeep_run())}
        self._tasks["startup_timeout"] = {asyncio.create_task(self._startup_timeout())}

        self._iopub_server, self._iopub_port = await self._start_one_server(
            self._iopub_listen
        )
        self._heartbeat_server, self._heartbeat_port = await self._start_one_server(
            self._heartbeat_listen
        )
        self._control_server, self._control_port = await self._start_one_server(
            self._control_listen
        )
        self._stdin_server, self._stdin_port = await self._start_one_server(
            self._stdin_listen
        )
        self._shell_server, self._shell_port = await self._start_one_server(
            self._shell_listen
        )

        #
        # For debugging, can use the real ZMQ library instead on certain sockets; comment out
        # the corresponding asyncio.start_server() call above if you enable the ZMQ-based
        # functions here.  You can then turn of verbosity level 4 (-vvvv) in hass_pyscript_kernel.py
        # to see all the byte data in case you need to debug the simple ZMQ implementation here.
        # The two most important zmq functions are shown below.
        #
        #  import zmq
        #  import zmq.asyncio
        #
        #  def zmq_bind(socket, connection, port):
        #      """Bind a socket."""
        #      if port <= 0:
        #          return socket.bind_to_random_port(connection)
        #      # _LOGGER.debug(f"binding to %s:%s" % (connection, port))
        #      socket.bind("%s:%s" % (connection, port))
        #      return port
        #
        #  zmq_ctx = zmq.asyncio.Context()
        #
        #  ##########################################
        #  # Shell using real ZMQ for debugging:
        #  async def shell_listen_zmq():
        #      """Task that listens to shell messages using ZMQ."""
        #      try:
        #          _LOGGER.debug("shell_listen_zmq connected")
        #          connection = self.config["transport"] + "://" + self.config["ip"]
        #          shell_socket = zmq_ctx.socket(zmq.ROUTER)
        #          self.shell_port = zmq_bind(shell_socket, connection, -1)
        #          _LOGGER.debug("shell_listen_zmq connected")
        #          while 1:
        #              msg = await shell_socket.recv_multipart()
        #              await self.shell_handler(shell_socket, msg)
        #      except asyncio.CancelledError:
        #          raise
        #      except Exception:
        #          _LOGGER.error("shell_listen exception %s", traceback.format_exc(-1))
        #          await self.housekeep_q.put(["shutdown"])
        #
        #  ##########################################
        #  # IOPub using real ZMQ for debugging:
        #  # IOPub/Sub:
        #  async def iopub_listen_zmq():
        #      """Task that listens to iopub messages using ZMQ."""
        #      try:
        #          _LOGGER.debug("iopub_listen_zmq connected")
        #          connection = self.config["transport"] + "://" + self.config["ip"]
        #          iopub_socket = zmq_ctx.socket(zmq.PUB)
        #          self.iopub_port = zmq_bind(self.iopub_socket, connection, -1)
        #          self.iopub_socket.add(iopub_socket)
        #          while 1:
        #              wire_msg = await iopub_socket.recv_multipart()
        #              _LOGGER.debug("iopub received %s", wire_msg)
        #      except asyncio.CancelledError:
        #          raise
        #      except EOFError:
        #          await self.housekeep_q.put(["shutdown"])
        #          _LOGGER.debug("iopub_listen got eof")
        #      except Exception as err:
        #          _LOGGER.error("iopub_listen exception %s", err)
        #          await self.housekeep_q.put(["shutdown"])
        #
        # self.tasks["shell"] = {asyncio.create_task(shell_listen_zmq())}
        # self.tasks["iopub"] = {asyncio.create_task(iopub_listen_zmq())}
        #

    async def session_shutdown(self):
        """Shutdown the kernel session."""
        if not self._iopub_server:
            # already shutdown, so quit
            return
        self._ast_ctx.global_ctx.close()
        self._ast_ctx.remove_logger_handler(self._console)
        _LOGGER.info(f"Shutting down session {self._ast_ctx.global_ctx.name}")

        for server in [
            self._heartbeat_server,
            self._control_server,
            self._stdin_server,
            self._shell_server,
            self._iopub_server,
        ]:
            if server:
                server.close()
        self._heartbeat_server = None
        self._iopub_server = None
        self._control_server = None
        self._stdin_server = None
        self._shell_server = None

        for task_set in self._tasks.values():
            for task in task_set:
                try:
                    task.cancel()
                    await task
                except asyncio.CancelledError:
                    pass
        self._tasks = []

        for sock in self._iopub_socket:
            try:
                sock.close()
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.error(f"iopub socket close exception: {err}")

        self._iopub_socket = set()


def _msg_id():
    """Return a new uuid for message id."""
    return str(uuid.uuid4())


def _str_to_bytes(string):
    """Encode a string in bytes."""
    return string.encode("utf-8")
