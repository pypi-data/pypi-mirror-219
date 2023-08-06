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
import traceback
import typing

from ... import core
from .ast_eval import AstEval

if not typing.TYPE_CHECKING:

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .pyscript_component import PyscriptComponent


_LOGGER: typing.Final = logging.getLogger(__package__ + ".function")


# pylint: disable=unused-variable
class Functions:
    """Define function handler functions."""

    def __init__(self, owner: PyscriptComponent):
        """Initialize Function."""
        self._owner = owner

        #
        # initial list of available functions
        #
        self._functions = {
            "event.fire": self._event_fire,
            "service.call": self._service_call,
            "service.has_service": self._service_has_service,
            "task.cancel": self._user_task_cancel,
            "task.current_task": self._user_task_current_task,
            "task.remove_done_callback": self._user_task_remove_done_callback,
            "task.sleep": self._async_sleep,
            "task.wait": self._user_task_wait,
        }

        #
        # Functions that take the AstEval context as a first argument,
        # which is needed by a handful of special functions that need the
        # ast context
        #
        self._ast_functions = {
            "log.debug": lambda ast_ctx: ast_ctx.logger.debug,
            "log.error": lambda ast_ctx: ast_ctx.logger.error,
            "log.info": lambda ast_ctx: ast_ctx.logger.info,
            "log.warning": lambda ast_ctx: ast_ctx.logger.warning,
            "print": lambda ast_ctx: ast_ctx.logger.debug,
            "task.name2id": self._task_name2id_factory,
            "task.unique": self.task_unique_factory,
        }

        #
        # Mappings of tasks ids <-> task names
        #
        self._unique_task2name: dict[asyncio.Task, set[str]] = {}
        self._unique_name2task: dict[str, asyncio.Task] = {}

        #
        # Mappings of task id to hass contexts
        self._task2context: dict[asyncio.Task, core.Context] = {}

        #
        # Set of tasks that are running
        #
        self._our_tasks: set[asyncio.Task] = set()

        #
        # Done callbacks for each task
        #
        # for each task:
        #   'ctx' -> ast_ctx
        #   'cb' -> dict[callback, tuple[ast_ctx, args, kwargs]]
        self._task2cb: dict[asyncio.Task, dict[str, typing.Any]] = {}

        #
        # reference counting for service registrations; the new @service trigger
        # registers the service call before the old one is removed, so we only
        # remove the service registration when the reference count goes to zero
        #
        self._service_cnt = {}

        #
        # save the global_ctx name where a service is registered so we can raise
        # an exception if it gets registered by a different global_ctx.
        #
        self._service2global_ctx = {}

        #
        # start a task which is a reaper for canceled tasks, since some # functions
        # like TrigInfo.stop() can't be async (it's called from a __del__ method)
        #
        async def task_reaper(reaper_q: asyncio.Queue):
            while True:
                try:
                    cmd = await reaper_q.get()
                    if cmd[0] == "exit":
                        return
                    if cmd[0] == "cancel":
                        try:
                            cmd[1].cancel()
                            await cmd[1]
                        except asyncio.CancelledError:
                            pass
                    else:
                        _LOGGER.error(f"task_reaper: unknown command {cmd[0]}")
                except asyncio.CancelledError:  # pylint: disable=try-except-raise
                    raise
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.error(
                        f"task_reaper: got exception {traceback.format_exc(-1)}"
                    )

        #
        # task id of the task that cancels and waits for other tasks,
        #
        self._task_reaper_q: asyncio.Queue = asyncio.Queue(0)
        self._task_reaper = self.create_task(task_reaper(self._task_reaper_q))

        #
        # start a task which creates tasks to run coros, and then syncs on their completion;
        # this is used by the shutdown trigger
        #
        async def task_waiter(waiter_q: asyncio.Queue):
            aws = []
            while True:
                try:
                    cmd = await waiter_q.get()
                    if cmd[0] == "exit":
                        return
                    if cmd[0] == "await":
                        aws.append(self.create_task(cmd[1]))
                    elif cmd[0] == "sync":
                        if len(aws) > 0:
                            await asyncio.gather(*aws)
                            aws = []
                        await cmd[1].put(0)
                    else:
                        _LOGGER.error(f"task_waiter: unknown command {cmd[0]}")
                except asyncio.CancelledError:  # pylint: disable=try-except-raise
                    raise
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.error(
                        f"task_waiter: got exception {traceback.format_exc(-1)}"
                    )

        #
        # task id of the task that awaits for coros (used by shutdown triggers)
        #
        self._task_waiter_q = asyncio.Queue(0)
        self._task_waiter = self.create_task(task_waiter(self._task_waiter_q))

    @property
    def controller(self) -> core.SmartHomeController:
        if not self._owner:
            return None
        return self._owner.controller

    def reaper_cancel(self, task: asyncio.Task):
        """Send a task to be canceled by the reaper."""
        self._task_reaper_q.put_nowait(["cancel", task])

    async def reaper_stop(self):
        """Tell the reaper task to exit."""
        if self._task_reaper:
            self._task_reaper_q.put_nowait(["exit"])
            await self._task_reaper
            self._task_reaper = None
            self._task_reaper_q = None

    def waiter_await(self, coro: typing.Coroutine):
        """Send a coro to be awaited by the waiter task."""
        self._task_waiter_q.put_nowait(["await", coro])

    async def waiter_sync(self):
        """Wait until the waiter queue is empty."""
        if self._task_waiter:
            sync_q = asyncio.Queue(0)
            self._task_waiter_q.put_nowait(["sync", sync_q])
            await sync_q.get()

    async def waiter_stop(self):
        """Tell the waiter task to exit."""
        if self._task_waiter:
            self._task_waiter_q.put_nowait(["exit"])
            await self._task_waiter
            self._task_waiter = None
            self._task_waiter_q = None

    async def _async_sleep(self, duration):
        """Implement task.sleep()."""
        await asyncio.sleep(float(duration))

    async def _event_fire(self, event_type: str, **kwargs):
        """Implement event.fire()."""
        curr_task = asyncio.current_task()
        context = kwargs.get("context")
        if isinstance(context, core.Context):
            del kwargs["context"]
        else:
            context = self._task2context.get(curr_task, None)

        self.controller.bus.async_fire(event_type, kwargs, context=context)

    def store_context(self, context: core.Context):
        """Store a context against the running task."""
        curr_task = asyncio.current_task()
        self._task2context[curr_task] = context

    def task_unique_factory(self, ctx: AstEval):
        """Define and return task.unique() for this context."""

        async def task_unique(name: str, kill_me=False):
            """Implement task.unique()."""
            name = f"{ctx.global_ctx.name}.{name}"
            curr_task = asyncio.current_task()
            task = self._unique_name2task.get(name)
            if task:
                if kill_me:
                    if task != curr_task:
                        #
                        # it seems we can't cancel ourselves, so we
                        # tell the reaper task to cancel us
                        #
                        self.reaper_cancel(curr_task)
                        # wait to be canceled
                        await asyncio.sleep(100000)
                elif task != curr_task and task in self._our_tasks:
                    # only cancel tasks if they are ones we started
                    self.reaper_cancel(task)
            if curr_task in self._our_tasks:
                if task:
                    if task in self._unique_task2name:
                        self._unique_task2name[task].discard(name)
                self._unique_name2task[name] = curr_task
                if curr_task not in self._unique_task2name:
                    self._unique_task2name[curr_task] = set()
                self._unique_task2name[curr_task].add(name)

        return task_unique

    async def _user_task_cancel(self, task: asyncio.Task = None):
        """Implement task.cancel()."""
        do_sleep = False
        if not task:
            task = asyncio.current_task()
            do_sleep = True
        if task not in self._our_tasks:
            raise TypeError(f"{task} is not a user-started task")
        self.reaper_cancel(task)
        if do_sleep:
            # wait to be canceled
            await asyncio.sleep(100000)

    async def _user_task_current_task(self):
        """Implement task.current_task()."""
        return asyncio.current_task()

    def _task_name2id_factory(self, ctx: AstEval):
        """Define and return task.name2id() for this context."""

        def user_task_name2id(name: str = None):
            """Implement task.name2id()."""
            prefix = f"{ctx.global_ctx.name}."
            if name is None:
                ret = {}
                for task_name, task_id in self._unique_name2task.items():
                    if task_name.startswith(prefix):
                        ret[task_name[len(prefix) :]] = task_id
                return ret
            result = self._unique_name2task.get(prefix + name)
            if result:
                return result
            raise NameError(f"task name '{name}' is unknown")

        return user_task_name2id

    async def _user_task_wait(self, aws: typing.Iterable[asyncio.Task], **kwargs):
        """Implement task.wait()."""
        return await asyncio.wait(aws, **kwargs)

    def _user_task_remove_done_callback(self, task: asyncio.Task, callback):
        """Implement task.remove_done_callback()."""
        self._task2cb[task]["cb"].pop(callback, None)

    def unique_name_used(self, ctx: AstEval, name: str):
        """Return whether the current unique name is in use."""
        name = f"{ctx.global_ctx.name()}.{name}"
        return name in self._unique_name2task

    def _service_has_service(self, domain: str, name: str):
        """Implement service.has_service()."""
        return self.controller.services.has_service(domain, name)

    async def _service_call(self, domain: str, name: str, **kwargs):
        """Implement service.call()."""
        curr_task = asyncio.current_task()
        args = {}
        for keyword, typ, default in [
            ("context", [core.Context], self._task2context.get(curr_task, None)),
            ("blocking", [bool], None),
            ("limit", [float, int], None),
        ]:
            if keyword in kwargs and type(kwargs[keyword]) in typ:
                args[keyword] = kwargs.pop(keyword)
            elif default:
                args[keyword] = default

        await self.controller.services.async_call(domain, name, kwargs, **args)

    async def service_completions(self, root: str):
        """Return possible completions of HASS services."""
        words = set()
        services = self.controller.services.async_services()
        num_period = root.count(".")
        if num_period == 1:
            domain, svc_root = root.split(".")
            if domain in services:
                words |= {
                    f"{domain}.{svc}"
                    for svc in services[domain]
                    if svc.lower().startswith(svc_root)
                }
        elif num_period == 0:
            words |= {domain for domain in services if domain.lower().startswith(root)}

        return words

    async def func_completions(self, root: str):
        """Return possible completions of functions."""
        funcs = {**self._functions, **self._ast_functions}
        words = {name for name in funcs if name.lower().startswith(root)}

        return words

    def register(self, funcs: dict):
        """Register functions to be available for calling."""
        self._functions.update(funcs)

    def register_ast(self, funcs: dict):
        """Register functions that need ast context to be available for calling."""
        self._ast_functions.update(funcs)

    def install_ast_funcs(self, ast_ctx: AstEval):
        """Install ast functions into the local symbol table."""
        sym_table = {name: func(ast_ctx) for name, func in self._ast_functions.items()}
        ast_ctx.set_local_sym_table(sym_table)

    def get(self, name):
        """Lookup a function locally and then as a service."""
        func = self._functions.get(name, None)
        if func:
            return func

        name_parts = name.split(".")
        if len(name_parts) != 2:
            return None

        domain, service = name_parts
        if not self._service_has_service(domain, service):
            return None

        def service_call_factory(domain, service):
            async def service_call(*args, **kwargs):
                curr_task = asyncio.current_task()
                service_args = {}
                for keyword, typ, default in [
                    (
                        "context",
                        [core.Context],
                        self._task2context.get(curr_task, None),
                    ),
                    ("blocking", [bool], None),
                    ("limit", [float, int], None),
                ]:
                    if keyword in kwargs and type(kwargs[keyword]) in typ:
                        service_args[keyword] = kwargs.pop(keyword)
                    elif default:
                        service_args[keyword] = default

                if len(args) != 0:
                    raise TypeError(
                        f"service {domain}.{service} takes only keyword arguments"
                    )

                await self.controller.services.async_call(
                    domain, service, kwargs, **service_args
                )

            return service_call

        return service_call_factory(domain, service)

    async def _run_coro(self, coro: typing.Coroutine, ast_ctx: AstEval = None):
        """Run coroutine task and update unique task on start and exit."""
        #
        # Add a placeholder for the new task so we know it's one we started
        #
        task: asyncio.Task = None
        try:
            task = asyncio.current_task()
            self._our_tasks.add(task)
            if ast_ctx is not None:
                self.task_done_callback_ctx(task, ast_ctx)
            result = await coro
            return result
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error(f"run_coro: got exception {traceback.format_exc(-1)}")
        finally:
            if task in self._task2cb:
                for callback, info in self._task2cb[task]["cb"].items():
                    ast_ctx, args, kwargs = info
                    await ast_ctx.call_func(callback, None, *args, **kwargs)
                    if ast_ctx.get_exception_obj():
                        ast_ctx.logger.error(ast_ctx.get_exception_long())
                        break
            if task in self._unique_task2name:
                for name in self._unique_task2name[task]:
                    del self._unique_name2task[name]
                del self._unique_task2name[task]
            self._task2context.pop(task, None)
            self._task2cb.pop(task, None)
            self._our_tasks.discard(task)

    def create_task(
        self, coro: typing.Coroutine, ast_ctx: AstEval = None
    ) -> asyncio.Task:
        """Create a new task that runs a coroutine."""
        return self.controller.async_create_task(
            self._run_coro(coro, ast_ctx=ast_ctx), True
        )

    def service_register(
        self, global_ctx_name: str, domain: str, service: str, callback
    ):
        """Register a new service callback."""
        key = f"{domain}.{service}"
        if key not in self._service2global_ctx:
            self._service2global_ctx[key] = global_ctx_name
        if self._service2global_ctx[key] != global_ctx_name:
            raise ValueError(
                f"{global_ctx_name}: can't register service {key}; already defined in "
                + f"{self._service2global_ctx[key]}"
            )
        counter = self._service_cnt.get(key, 0)
        self._service_cnt[key] = counter + 1
        if counter == 0:
            self.controller.services.async_register(domain, service, callback)

    def service_remove(self, global_ctx_name, domain, service):
        """Remove a service callback."""
        key = f"{domain}.{service}"
        registered_ctx_name = self._service2global_ctx.get(key)
        if not registered_ctx_name or registered_ctx_name != global_ctx_name:
            return
        counter = self._service_cnt.get(key, 0)
        if counter > 1:
            self._service_cnt[key] = counter - 1
            return
        self._service_cnt[key] = 0
        self._service2global_ctx.pop(key, None)
        if counter == 1:
            self.controller.services.async_remove(domain, service)

    def task_done_callback_ctx(self, task: asyncio.Task, ast_ctx: AstEval):
        """Set the ast_ctx for a task, which is needed for done callbacks."""
        if task not in self._task2cb or "ctx" not in self._task2cb[task]:
            self._task2cb[task] = {"ctx": ast_ctx, "cb": {}}

    def task_add_done_callback(
        self, task: asyncio.Task, ast_ctx: AstEval, callback, *args, **kwargs
    ):
        """Add a done callback to the given task."""
        if ast_ctx is None:
            ast_ctx = self._task2cb[task]["ctx"]
        self._task2cb[task]["cb"][callback] = [ast_ctx, args, kwargs]

    def get_task_context(self, task: asyncio.Task = None) -> core.Context:
        if task is None:
            task = asyncio.current_task()
        return self._task2context.get(task, None)
