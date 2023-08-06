"""
Core components of Smart Home - The Next Generation.

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
import contextlib
import functools
import json
import logging
import re
import sys
import typing
from ast import literal_eval

import jinja2
import voluptuous as vol

from . import helpers
from .callback import callback
from .render_info import RenderInfo
from .result_wrapper import ResultWrapper
from .smart_home_controller_error import SmartHomeControllerError
from .template_context import template_context as context
from .template_environment import TemplateEnvironment
from .template_environment_type import TemplateEnvironmentType
from .template_error import TemplateError
from .template_vars_type import TemplateVarsType
from .thread_with_exception import ThreadWithException
from .tuple_wrapper import TupleWrapper


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_LOGGER: typing.Final = logging.getLogger(__name__)


class Template:
    """Class to hold a template and manage caching and rendering."""

    __slots__ = (
        "__weakref__",
        "_template",
        "_shc",
        "_is_static",
        "_compiled_code",
        "_compiled",
        "_exc_info",
        "_limited",
        "_strict",
    )

    _result_wrappers: dict[type, type] = {
        kls: ResultWrapper.gen_result_wrapper(kls)  # type: ignore[no-untyped-call]
        for kls in (list, dict, set)
    }
    _result_wrappers[tuple] = TupleWrapper

    _RE_JINJA_DELIMITERS: typing.Final = re.compile(r"\{%|\{\{|\{#")
    # Match "simple" ints and floats. -1.0, 1, +5, 5.0
    _IS_NUMERIC: typing.Final = re.compile(r"^[+-]?(?!0\d)\d*(?:\.\d*)?$")

    def __init__(self, template: str, shc: SmartHomeController = None):
        """Instantiate a template."""
        if not isinstance(template, str):
            raise TypeError("Expected template to be a string")

        self._template: str = template.strip()
        self._compiled_code = None
        self._compiled: jinja2.Template = None
        self._shc = shc
        self._is_static = not Template.is_template_string(template)
        self._exc_info = None
        self._limited = None
        self._strict = None

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    @controller.setter
    def controller(self, shc: SmartHomeController) -> None:
        if shc is None:
            return
        if self._shc is not None and self._shc is not shc:
            raise SmartHomeControllerError("There can be only one!")
        self._shc = shc

    @property
    def _env(self) -> TemplateEnvironment:
        if self._shc is None:
            wanted_env = TemplateEnvironmentType.NO_SHC
        elif self._limited:
            wanted_env = TemplateEnvironmentType.LIMITED
        elif self._strict:
            wanted_env = TemplateEnvironmentType.STRICT
        else:
            wanted_env = TemplateEnvironmentType.NORMAL

        return TemplateEnvironment.get_env(wanted_env, self._shc)

    @property
    def template_code(self) -> str:
        return self._template

    @property
    def is_static(self):
        return self._is_static

    def ensure_valid(self) -> None:
        """Return if template is valid."""
        with Template.set_template(self._template, "compiling"):
            if self._is_static or self._compiled_code is not None:
                return

            try:
                self._compiled_code = self._env.compile(self._template)
            except jinja2.TemplateError as err:
                raise TemplateError(err) from err

    def render(
        self,
        variables: TemplateVarsType = None,
        parse_result: bool = True,
        limited: bool = False,
        **kwargs: typing.Any,
    ) -> typing.Any:
        """Render given template.

        If limited is True, the template is not allowed to access any function
        or filter depending on tng or the state machine.
        """
        if self._is_static:
            if not parse_result or self._shc.config.legacy_templates:
                return self._template
            return self._parse_result(self._template)

        return self._shc.run_callback_threadsafe(
            functools.partial(
                self.async_render, variables, parse_result, limited, **kwargs
            ),
        ).result()

    @callback
    def async_render(
        self,
        variables: TemplateVarsType = None,
        parse_result: bool = True,
        limited: bool = False,
        strict: bool = False,
        **kwargs: typing.Any,
    ) -> typing.Any:
        """Render given template.

        This method must be run in the event loop.

        If limited is True, the template is not allowed to access any function or
        filter depending on tng or the state machine.
        """
        if self._is_static:
            if not parse_result or self._shc.config.legacy_templates:
                return self._template
            return self._parse_result(self._template)

        compiled = self._compiled or self._ensure_compiled(limited, strict)

        if variables is not None:
            kwargs.update(variables)

        try:
            render_result = Template._render_with_context(
                self._template, compiled, **kwargs
            )
        except Exception as err:
            raise TemplateError(err) from err

        render_result = render_result.strip()

        if self._shc.config.legacy_templates or not parse_result:
            return render_result

        return self._parse_result(render_result)

    @staticmethod
    def _parse_result(render_result: str) -> typing.Any:
        """Parse the result."""
        try:
            result = literal_eval(render_result)

            if type(result) in Template._result_wrappers:
                result = Template._result_wrappers[type(result)](
                    result, render_result=render_result
                )

            # If the literal_eval result is a string, use the original
            # render, by not returning right here. The evaluation of strings
            # resulting in strings impacts quotes, to avoid unexpected
            # output; use the original render instead of the evaluated one.
            # Complex and scientific values are also unexpected. Filter them out.
            if (
                # Filter out string and complex numbers
                not isinstance(result, (str, complex))
                and (
                    # Pass if not numeric and not a boolean
                    not isinstance(result, (int, float))
                    # Or it's a boolean (inherit from int)
                    or isinstance(result, bool)
                    # Or if it's a digit
                    or Template._IS_NUMERIC.match(render_result) is not None
                )
            ):
                return result
        except (ValueError, TypeError, SyntaxError, MemoryError):
            pass

        return render_result

    async def async_render_will_timeout(
        self,
        timeout: float,
        variables: TemplateVarsType = None,
        strict: bool = False,
        **kwargs: typing.Any,
    ) -> bool:
        """Check to see if rendering a template will timeout during render.

        This is intended to check for expensive templates
        that will make the system unstable.  The template
        is rendered in the executor to ensure it does not
        tie up the event loop.

        This function is not a security control and is only
        intended to be used as a safety check when testing
        templates.

        This method must be run in the event loop.
        """
        if self._is_static:
            return False

        compiled = self._compiled or self._ensure_compiled(strict=strict)

        if variables is not None:
            kwargs.update(variables)

        self._exc_info = None
        finish_event = asyncio.Event()

        async def _templated_rendered():
            finish_event.set()

        def _render_template() -> None:
            try:
                Template._render_with_context(self._template, compiled, **kwargs)
            except TimeoutError:
                pass
            except Exception:  # pylint: disable=broad-except
                self._exc_info = sys.exc_info()
            finally:
                self._shc.run_coroutine_threadsafe(_templated_rendered())

        try:
            template_render_thread = ThreadWithException(target=_render_template)
            template_render_thread.start()
            await asyncio.wait_for(finish_event.wait(), timeout=timeout)
            if self._exc_info:
                raise TemplateError(self._exc_info[1].with_traceback(self._exc_info[2]))
        except asyncio.TimeoutError:
            template_render_thread.raise_exc(TimeoutError)
            return True
        finally:
            template_render_thread.join()

        return False

    @callback
    def async_render_to_info(
        self,
        variables: TemplateVarsType = None,
        strict: bool = False,
        **kwargs: typing.Any,
    ) -> RenderInfo:
        """Render the template and collect an entity filter."""

        # pylint: disable=protected-access
        assert self._shc and RenderInfo.current() is None

        render_info = RenderInfo(self)

        if self._is_static:
            render_info.set_static_result(self._template.strip())
            return render_info

        try:
            render_info.set_result(
                self.async_render(variables, strict=strict, **kwargs)
            )
        except TemplateError as ex:
            render_info.set_result(ex)
        finally:
            RenderInfo._active_instance.instance = None

        render_info.freeze()

        return render_info

    def render_with_possible_json_value(
        self, value, error_value=TemplateEnvironment.SENTINEL
    ):
        """Render template with value exposed.

        If valid JSON will expose value_json too.
        """
        if self._is_static:
            return self._template

        return self._shc.run_callback_threadsafe(
            self.async_render_with_possible_json_value,
            value,
            error_value,
        ).result()

    @callback
    def async_render_with_possible_json_value(
        self, value, error_value=TemplateEnvironment.SENTINEL, variables=None
    ):
        """Render template with value exposed.

        If valid JSON will expose value_json too.

        This method must be run in the event loop.
        """
        if self._is_static:
            return self._template

        if self._compiled is None:
            self._ensure_compiled()

        variables = dict(variables or {})
        variables["value"] = value

        with contextlib.suppress(ValueError, TypeError):
            variables["value_json"] = json.loads(value)

        try:
            return Template._render_with_context(
                self._template, self._compiled, **variables
            ).strip()
        except jinja2.TemplateError as ex:
            if error_value is TemplateEnvironment.SENTINEL:
                _LOGGER.error(
                    f"Error parsing value: {ex} (value: {value}, template: {self._template})"
                )
            return value if error_value is TemplateEnvironment.SENTINEL else error_value

    def _ensure_compiled(
        self, limited: bool = False, strict: bool = False
    ) -> jinja2.Template:
        """Bind a template to a specific tng instance."""
        self.ensure_valid()

        assert self._shc is not None, "SmartHomeController variable not set on template"
        assert (
            self._limited is None or self._limited == limited
        ), "can't change between limited and non limited template"
        assert (
            self._strict is None or self._strict == strict
        ), "can't change between strict and non strict template"
        assert not (strict and limited), "can't combine strict and limited template"

        self._limited = limited
        self._strict = strict
        env = self._env

        self._compiled = jinja2.Template.from_code(
            env, self._compiled_code, env.globals, None
        )

        return self._compiled

    # pylint: disable=protected-access
    def __eq__(self, other):
        """Compare template with another."""
        return (
            self.__class__ == other.__class__
            and self._template == other._template
            and self._shc == other._shc
        )

    def __hash__(self) -> int:
        """Hash code for template."""
        return hash(self._template)

    def __repr__(self) -> str:
        """Representation of Template."""
        return 'Template("' + self._template + '")'

    @contextlib.contextmanager
    @staticmethod
    def set_template(template_str: str, action: str) -> collections.abc.Generator:
        """Store template being parsed or rendered in a Contextvar to aid error handling."""
        context.set((template_str, action))
        try:
            yield
        finally:
            context.set(None)

    @staticmethod
    def _render_with_context(
        template_str: str, template: jinja2.Template, **kwargs: typing.Any
    ) -> str:
        """Store template being rendered in a ContextVar to aid error handling."""
        with Template.set_template(template_str, "rendering"):
            return template.render(**kwargs)

    @staticmethod
    def result_as_boolean(template_result: typing.Any) -> bool:
        """Convert the template result to a boolean.

        True/not 0/'1'/'true'/'yes'/'on'/'enable' are considered truthy
        False/0/None/'0'/'false'/'no'/'off'/'disable' are considered falsy

        """
        if template_result is None:
            return False

        try:
            # pylint: disable=import-outside-toplevel
            return helpers.boolean(template_result)
        except vol.Invalid:
            return False

    @staticmethod
    def attach(shc: SmartHomeController, obj: typing.Any) -> None:
        """Recursively attach hass to all template instances in list and dict."""
        if isinstance(obj, list):
            for child in obj:
                Template.attach(shc, child)
        elif isinstance(obj, collections.abc.Mapping):
            for child_key, child_value in obj.items():
                Template.attach(shc, child_key)
                Template.attach(shc, child_value)
        elif isinstance(obj, Template):
            typing.cast(Template, obj)._shc = shc

    @staticmethod
    def render_complex(
        value: typing.Any,
        variables: TemplateVarsType = None,
        limited: bool = False,
        parse_result: bool = True,
    ) -> typing.Any:
        """Recursive template creator helper function."""
        if isinstance(value, list):
            return [
                Template.render_complex(item, variables, limited, parse_result)
                for item in value
            ]
        if isinstance(value, collections.abc.Mapping):
            return {
                Template.render_complex(
                    key, variables, limited, parse_result
                ): Template.render_complex(item, variables, limited, parse_result)
                for key, item in value.items()
            }
        if isinstance(value, Template):
            return value.async_render(
                variables, limited=limited, parse_result=parse_result
            )

        return value

    @staticmethod
    def is_complex(value: typing.Any) -> bool:
        """Test if data structure is a complex template."""
        if isinstance(value, Template):
            return True
        if isinstance(value, list):
            return any(Template.is_complex(val) for val in value)
        if isinstance(value, collections.abc.Mapping):
            return any(Template.is_complex(val) for val in value.keys()) or any(
                Template.is_complex(val) for val in value.values()
            )
        return False

    @staticmethod
    def is_template_string(maybe_template: str) -> bool:
        """Check if the input is a Jinja2 template."""
        return Template._RE_JINJA_DELIMITERS.search(maybe_template) is not None
