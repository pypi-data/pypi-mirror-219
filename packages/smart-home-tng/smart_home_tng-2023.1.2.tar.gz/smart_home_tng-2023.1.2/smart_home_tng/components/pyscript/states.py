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
from .pyscript_entity import PyscriptEntity
from .state_val import StateVal

if not typing.TYPE_CHECKING:

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .pyscript_component import PyscriptComponent

_LOGGER: typing.Final = logging.getLogger(__package__ + ".state")
_STATE_VIRTUAL_ATTRS: typing.Final = {"last_changed", "last_updated"}


# pylint: disable=unused-variable
class States:
    """Class for state functions."""

    def __init__(self, owner: PyscriptComponent):
        """Initialize States."""
        self._owner = owner

        #
        # notify message queues by variable
        #
        self._notify: dict[typing.Any, dict[asyncio.Queue, typing.Any]] = {}

        #
        # Last value of state variable notifications.  We maintain this
        # so that trigger evaluation can use the last notified value,
        # rather than fetching the current value, which is subject to
        # race conditions when multiple state variables are set quickly.
        #
        self._notify_var_last = {}

        #
        # pyscript vars which have already been registered as persisted
        #
        self._persisted_vars: dict[str, PyscriptEntity] = {}

        #
        # other parameters of all services that have "entity_id" as a parameter
        #
        self._service2args = {}

    @property
    def controller(self):
        return self._owner.controller

    @property
    def pyscript(self):
        return self._owner

    async def get_service_params(self):
        """Get parameters for all services."""
        self._service2args = {}
        all_services = await core.Service.async_get_all_descriptions(self.controller)
        for domain, services in all_services.items():
            self._service2args[domain] = {}
            for service, desc in services.items():
                if "entity_id" not in desc["fields"] and "target" not in desc:
                    continue
                self._service2args[domain][service] = set(desc["fields"].keys())
                self._service2args[domain][service].discard("entity_id")

    async def notify_add(self, var_names, queue: asyncio.Queue):
        """Register to notify state variables changes to be sent to queue."""

        added = False
        for var_name in var_names if isinstance(var_names, set) else {var_names}:
            parts = var_name.split(".")
            if len(parts) != 2 and len(parts) != 3:
                continue
            state_var_name = f"{parts[0]}.{parts[1]}"
            if state_var_name not in self._notify:
                self._notify[state_var_name] = {}
            self._notify[state_var_name][queue] = var_names
            added = True
        return added

    def notify_del(self, var_names, queue: asyncio.Queue):
        """Unregister notify of state variables changes for given queue."""

        for var_name in var_names if isinstance(var_names, set) else {var_names}:
            parts = var_name.split(".")
            if len(parts) != 2 and len(parts) != 3:
                continue
            state_var_name = f"{parts[0]}.{parts[1]}"
            if state_var_name not in self._notify:
                return
            self._notify[state_var_name].pop(queue, None)

    async def update(self, new_vars: dict, func_args):
        """Deliver all notifications for state variable changes."""

        notify: dict[asyncio.Queue, typing.Any] = {}
        for var_name, var_val in new_vars.items():
            if var_name in self._notify:
                self._notify_var_last[var_name] = var_val
                notify.update(self._notify[var_name])

        if notify:
            _LOGGER.debug(f"state.update({new_vars}, {func_args})")
            for queue, var_names in notify.items():
                await queue.put(
                    ["state", [self.notify_var_get(var_names, new_vars), func_args]]
                )

    def notify_var_get(self, var_names, new_vars):
        """Add values of var_names to new_vars, or default to None."""
        notify_vars = new_vars.copy()
        for var_name in var_names if var_names is not None else []:
            if var_name in notify_vars:
                continue
            parts = var_name.split(".")
            if var_name in self._notify_var_last:
                notify_vars[var_name] = self._notify_var_last[var_name]
            elif len(parts) == 3 and f"{parts[0]}.{parts[1]}" in self._notify_var_last:
                notify_vars[var_name] = getattr(
                    self._notify_var_last[f"{parts[0]}.{parts[1]}"], parts[2], None
                )
            elif (
                len(parts) == 4
                and parts[2] == "old"
                and f"{parts[0]}.{parts[1]}.old" in notify_vars
            ):
                notify_vars[var_name] = getattr(
                    notify_vars[f"{parts[0]}.{parts[1]}.old"], parts[3], None
                )
            elif 1 <= var_name.count(".") <= 3 and not self.exist(var_name):
                notify_vars[var_name] = None
        return notify_vars

    def set(self, var_name: str, value=None, new_attributes=None, **kwargs):
        """Set a state variable and optional attributes in SmartHomeController."""
        if var_name.count(".") != 1:
            raise NameError(f"invalid name {var_name} (should be 'domain.entity')")

        if isinstance(value, StateVal):
            if new_attributes is None:
                #
                # value is a StateVal, so extract the attributes and value
                #
                new_attributes = value.__dict__.copy()
                for discard in _STATE_VIRTUAL_ATTRS:
                    new_attributes.pop(discard, None)
            value = str(value)

        state_value = None
        if value is None or new_attributes is None:
            state_value = self.controller.states.get(var_name)

        if value is None and state_value:
            value = state_value.state

        if new_attributes is None:
            if state_value:
                new_attributes = state_value.attributes.copy()
            else:
                new_attributes = {}

        context = kwargs.get("context", None)
        if isinstance(context, core.Context):
            kwargs.pop("context")
        else:
            context = self.pyscript.functions.get_task_context()

        if kwargs:
            new_attributes = new_attributes.copy()
            new_attributes.update(kwargs)

        _LOGGER.debug(f"setting {var_name} = {value}, attr = {new_attributes}")
        self.controller.states.async_set(
            var_name, value, new_attributes, context=context
        )
        if var_name in self._notify_var_last or var_name in self._notify:
            #
            # immediately update a variable we are monitoring since it could take a while
            # for the state changed event to propagate
            #
            self._notify_var_last[var_name] = StateVal(
                self.controller.states.get(var_name)
            )

        if var_name in self._persisted_vars:
            self._persisted_vars[var_name].set_state(value)
            self._persisted_vars[var_name].set_attributes(new_attributes)

    def setattr(self, var_attr_name: str, value):
        """Set a state variable's attribute in hass."""
        parts = var_attr_name.split(".")
        if len(parts) != 3:
            raise NameError(
                f"invalid name {var_attr_name} (should be 'domain.entity.attr')"
            )
        if not self.exist(f"{parts[0]}.{parts[1]}"):
            raise NameError(f"state {parts[0]}.{parts[1]} doesn't exist")
        self.set(f"{parts[0]}.{parts[1]}", **{parts[2]: value})

    async def register_persist(self, var_name: str):
        """Register pyscript state variable to be persisted with RestoreState."""
        if var_name.startswith("pyscript.") and var_name not in self._persisted_vars:
            restore_data = await core.RestoreStateData.async_get_instance(
                self.controller
            )
            this_entity = PyscriptEntity(var_name)
            self._persisted_vars[var_name] = this_entity
            try:
                restore_data.async_restore_entity_added(this_entity)
            except TypeError:
                restore_data.async_restore_entity_added(var_name)

    async def persist(self, var_name: str, default_value=None, default_attributes=None):
        """Persist a pyscript domain state variable, and update with optional defaults."""
        if var_name.count(".") != 1 or not var_name.startswith("pyscript."):
            raise NameError(f"invalid name {var_name} (should be 'pyscript.entity')")

        await self.register_persist(var_name)
        exists = self.exist(var_name)

        if not exists and default_value is not None:
            self.set(var_name, default_value, default_attributes)
        elif exists and default_attributes is not None:
            # Patch the attributes with new values if necessary
            current = self.controller.states.get(var_name)
            new_attributes = {
                k: v
                for (k, v) in default_attributes.items()
                if k not in current.attributes
            }
            self.set(var_name, current.state, **new_attributes)

    def exist(self, var_name: str):
        """Check if a state variable value or attribute exists in hass."""
        parts = var_name.split(".")
        if len(parts) != 2 and len(parts) != 3:
            return False
        value = self.controller.states.get(f"{parts[0]}.{parts[1]}")
        if value is None:
            return False
        if (
            len(parts) == 2
            or (
                parts[0] in self._service2args
                and parts[2] in self._service2args[parts[0]]
            )
            or parts[2] in value.attributes
            or parts[2] in _STATE_VIRTUAL_ATTRS
        ):
            return True
        return False

    def get(self, var_name: str):
        """Get a state variable value or attribute from hass."""
        parts = var_name.split(".")
        if len(parts) != 2 and len(parts) != 3:
            raise NameError(
                f"invalid name '{var_name}' (should be 'domain.entity' or 'domain.entity.attr')"
            )
        state = self.controller.states.get(f"{parts[0]}.{parts[1]}")
        if not state:
            raise NameError(f"name '{parts[0]}.{parts[1]}' is not defined")
        #
        # simplest case is just the state value
        #
        state = StateVal(state)
        if len(parts) == 2:
            return state
        #
        # see if this is a service that has an entity_id parameter
        #
        if parts[0] in self._service2args and parts[2] in self._service2args[parts[0]]:
            params = self._service2args[parts[0]][parts[2]]

            def service_call_factory(domain: str, service: str, entity_id: str, params):
                async def service_call(*args, **kwargs):
                    service_args = {}
                    for keyword, typ, default in [
                        (
                            "context",
                            [core.Context],
                            self.pyscript.functions.get_task_context(),
                        ),
                        ("blocking", [bool], None),
                        ("limit", [float, int], None),
                    ]:
                        if keyword in kwargs and type(kwargs[keyword]) in typ:
                            service_args[keyword] = kwargs.pop(keyword)
                        elif default:
                            service_args[keyword] = default

                    kwargs["entity_id"] = entity_id
                    if len(args) == 1 and len(params) == 1:
                        #
                        # with just a single parameter and positional argument,
                        # create the keyword setting
                        #
                        [param_name] = params
                        kwargs[param_name] = args[0]
                    elif len(args) != 0:
                        raise TypeError(
                            f"service {domain}.{service} takes no positional arguments"
                        )
                    await self.controller.services.async_call(
                        domain, service, kwargs, **service_args
                    )

                return service_call

            return service_call_factory(
                parts[0], parts[2], f"{parts[0]}.{parts[1]}", params
            )
        #
        # finally see if it is an attribute
        #
        try:
            return getattr(state, parts[2])
        except AttributeError:
            raise AttributeError(  # pylint: disable=raise-missing-from
                f"state '{parts[0]}.{parts[1]}' has no attribute '{parts[2]}'"
            )

    def delete(self, var_name: str, context: core.Context = None):
        """Delete a state variable or attribute from hass."""
        parts = var_name.split(".")
        if not context:
            context = self.pyscript.functions.get_task_context()
        context_arg = {"context": context} if context else {}
        if len(parts) == 2:
            if var_name in self._notify_var_last or var_name in self._notify:
                #
                # immediately update a variable we are monitoring since it could take a while
                # for the state changed event to propagate
                #
                self._notify_var_last[var_name] = None
            if not self.controller.states.async_remove(var_name, **context_arg):
                raise NameError(f"name '{var_name}' not defined")
            return
        if len(parts) == 3:
            var_name = f"{parts[0]}.{parts[1]}"
            value = self.controller.states.get(var_name)
            if value is None:
                raise NameError(f"state {var_name} doesn't exist")
            new_attr = value.attributes.copy()
            if parts[2] not in new_attr:
                raise AttributeError(
                    f"state '{var_name}' has no attribute '{parts[2]}'"
                )
            del new_attr[parts[2]]
            self.set(f"{var_name}", value.state, new_attributes=new_attr, **context_arg)
            return
        raise NameError(
            f"invalid name '{var_name}' (should be 'domain.entity' or 'domain.entity.attr')"
        )

    def getattr(self, var_name: str):
        """Return a dict of attributes for a state variable."""
        if isinstance(var_name, StateVal):
            attrs = var_name.__dict__.copy()
            for discard in _STATE_VIRTUAL_ATTRS:
                attrs.pop(discard, None)
            return attrs
        if var_name.count(".") != 1:
            raise NameError(f"invalid name {var_name} (should be 'domain.entity')")
        value = self.controller.states.get(var_name)
        if not value:
            return None
        return value.attributes.copy()

    def completions(self, root):
        """Return possible completions of state variables."""
        words = set()
        parts = root.split(".")
        num_period = len(parts) - 1
        if num_period == 2:
            #
            # complete state attributes
            #
            last_period = root.rfind(".")
            name = root[0:last_period]
            value = self.controller.states.get(name)
            if value:
                attr_root = root[last_period + 1 :]
                attrs = set(value.attributes.keys()).union(_STATE_VIRTUAL_ATTRS)
                if parts[0] in self._service2args:
                    attrs.update(set(self._service2args[parts[0]].keys()))
                for attr_name in attrs:
                    if attr_name.lower().startswith(attr_root):
                        words.add(f"{name}.{attr_name}")
        elif num_period < 2:
            #
            # complete among all state names
            #
            for name in self.controller.states.async_all():
                if name.entity_id.lower().startswith(root):
                    words.add(name.entity_id)
        return words

    async def names(self, domain: str = None):
        """Implement names, which returns all entity_ids."""
        return self.controller.states.async_entity_ids(domain)

    def register_functions(self):
        """Register state functions and config variable."""
        functions = {
            "state.get": self.get,
            "state.set": self.set,
            "state.setattr": self.setattr,
            "state.names": self.names,
            "state.getattr": self.getattr,
            "state.persist": self.persist,
            "state.delete": self.delete,
            "pyscript.config": self.pyscript.config_data,
        }
        self.pyscript.functions.register(functions)
