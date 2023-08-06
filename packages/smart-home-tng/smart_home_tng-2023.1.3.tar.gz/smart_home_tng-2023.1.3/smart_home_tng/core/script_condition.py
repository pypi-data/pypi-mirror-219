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
import collections
import collections.abc
import datetime
import functools
import re
import typing

import voluptuous as vol

from smart_home_tng.core.platform import Platform

from . import helpers
from .action_condition_platform import ActionConditionPlatform
from .callback import callback
from .condition_checker_type import ConditionCheckerType
from .condition_error import ConditionError
from .condition_error_container import ConditionErrorContainer
from .condition_error_index import ConditionErrorIndex
from .condition_error_message import ConditionErrorMessage
from .config_type import ConfigType
from .config_validation import ConfigValidation as cv
from .const import Const
from .invalid_device_automation_config import InvalidDeviceAutomationConfig
from .location_info import LocationInfo
from .sensor import Sensor
from .singleton import Singleton
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError
from .state import State
from .sun import Sun
from .template import Template
from .template_error import TemplateError
from .template_vars_type import TemplateVarsType
from .trace import Trace

_INPUT_ENTITY_ID = re.compile(
    r"^input_(?:select|text|number|boolean|datetime)\.(?!.+__)(?!_)[\da-z_]+(?<!_)$"
)


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_ACTION_CONDITION_HELPER: typing.Final = Singleton()


# pylint: disable=unused-variable
class ScriptCondition(ActionConditionPlatform):
    """Helper for script conditions."""

    def __init__(self, shc: SmartHomeController) -> None:
        super().__init__()
        self._shc = shc

    @property
    def condition_schema(self) -> vol.Schema:
        return None

    async def async_get_condition_capabilities(
        self, config: ConfigType
    ) -> dict[str, vol.Schema] | collections.abc.Awaitable[dict[str, vol.Schema]]:
        return None

    async def async_get_conditions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | collections.abc.Awaitable[
        list[dict[str, typing.Any]]
    ]:
        return None

    @staticmethod
    @Singleton.shc_singleton(_ACTION_CONDITION_HELPER)
    def get_action_condition_protocol(
        shc: SmartHomeController,
    ) -> ActionConditionPlatform:
        return ScriptCondition(shc)

    @staticmethod
    async def async_automation_condition_from_config(
        shc: SmartHomeController, config: ConfigType
    ) -> ConditionCheckerType:
        prot = ScriptCondition.get_action_condition_protocol(shc)
        if isinstance(prot, ScriptCondition):
            return await prot.async_condition_from_config(config)
        raise NotImplementedError()

    async def async_condition_from_config(
        self, config: ConfigType
    ) -> ConditionCheckerType:
        """Turn a condition configuration into a method.

        Should be run on the event loop.
        """
        condition = str(config.get(Const.CONF_CONDITION)).lower()
        factory = None
        if condition == "and":
            factory = self.async_and_from_config
        elif condition == "or":
            factory = self.async_or_from_config
        elif condition == "not":
            factory = self.async_not_from_config
        elif condition == "device":
            factory = self.async_device_from_config
        elif condition == "numeric_state":
            factory = self.async_numeric_state_from_config
        elif condition == "state":
            factory = self.state_from_config
        elif condition == "sun":
            factory = self.sun_from_config
        elif condition == "template":
            factory = self.async_template_from_config
        elif condition == "time":
            factory = self.time_from_config
        elif condition == "trigger":
            factory = self.async_trigger_from_config
        elif condition == "zone":
            factory = self.zone_from_config
        else:
            raise SmartHomeControllerError(
                f'Invalid condition "{condition}" specified {config}'
            )

        # Check if condition is not enabled
        if not config.get(Const.CONF_ENABLED, True):

            @Trace.condition_function
            def disabled_condition(
                _shc: SmartHomeController, _variables: TemplateVarsType = None
            ) -> bool:
                """Condition not enabled, will always pass."""
                return True

            return disabled_condition

        # Check for partials to properly determine if coroutine function
        check_factory = factory
        while isinstance(check_factory, functools.partial):
            check_factory = check_factory.func

        if asyncio.iscoroutinefunction(check_factory):
            return await factory(config)
        return factory(config)

    async def async_and_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Create multi condition matcher using 'AND'."""
        checks = [
            await self.async_condition_from_config(entry)
            for entry in config["conditions"]
        ]

        @Trace.condition_function
        def if_and_condition(variables: TemplateVarsType = None) -> bool:
            """Test and condition."""
            errors = []
            for index, check in enumerate(checks):
                try:
                    with Trace.path(["conditions", str(index)]):
                        if not check(variables):
                            return False
                except ConditionError as ex:
                    errors.append(
                        ConditionErrorIndex(
                            "and", index=index, total=len(checks), error=ex
                        )
                    )

            # Raise the errors if no check was false
            if errors:
                raise ConditionErrorContainer("and", errors=errors)

            return True

        return if_and_condition

    async def async_or_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Create multi condition matcher using 'OR'."""
        checks = [
            await self.async_condition_from_config(entry)
            for entry in config["conditions"]
        ]

        @Trace.condition_function
        def if_or_condition(variables: TemplateVarsType = None) -> bool:
            """Test or condition."""
            errors = []
            for index, check in enumerate(checks):
                try:
                    with Trace.path(["conditions", str(index)]):
                        if check(self._shc, variables):
                            return True
                except ConditionError as ex:
                    errors.append(
                        ConditionErrorIndex(
                            "or", index=index, total=len(checks), error=ex
                        )
                    )

            # Raise the errors if no check was true
            if errors:
                raise ConditionErrorContainer("or", errors=errors)

            return False

        return if_or_condition

    async def async_not_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Create multi condition matcher using 'NOT'."""
        checks = [
            await self.async_condition_from_config(entry)
            for entry in config["conditions"]
        ]

        @Trace.condition_function
        def if_not_condition(variables: TemplateVarsType = None) -> bool:
            """Test not condition."""
            errors = []
            for index, check in enumerate(checks):
                try:
                    with Trace.path(["conditions", str(index)]):
                        if check(variables):
                            return False
                except ConditionError as ex:
                    errors.append(
                        ConditionErrorIndex(
                            "not", index=index, total=len(checks), error=ex
                        )
                    )

            # Raise the errors if no check was true
            if errors:
                raise ConditionErrorContainer("not", errors=errors)

            return True

        return if_not_condition

    def numeric_state(
        self,
        entity: str | State,
        below: float | str = None,
        above: float | str = None,
        value_template: Template = None,
        variables: TemplateVarsType = None,
    ) -> bool:
        """Test a numeric state condition."""
        return self._shc.run_callback_threadsafe(
            self.async_numeric_state,
            entity,
            below,
            above,
            value_template,
            variables,
        ).result()

    def async_numeric_state(
        self,
        entity: str | State,
        below: float | str = None,
        above: float | str = None,
        value_template: Template = None,
        variables: TemplateVarsType = None,
        attribute: str = None,
    ) -> bool:
        """Test a numeric state condition."""
        if entity is None:
            raise ConditionErrorMessage("numeric_state", "no entity specified")

        if isinstance(entity, str):
            entity_id = entity

            if (entity := self._shc.states.get(entity)) is None:
                raise ConditionErrorMessage(
                    "numeric_state", f"unknown entity {entity_id}"
                )
        else:
            entity_id = entity.entity_id

        if attribute is not None and attribute not in entity.attributes:
            Trace.set_condition_result(
                False,
                message=f"attribute '{attribute}' of entity {entity_id} does not exist",
            )
            return False

        value: typing.Any = None
        if value_template is None:
            if attribute is None:
                value = entity.state
            else:
                value = entity.attributes.get(attribute)
        else:
            variables = dict(variables or {})
            variables["state"] = entity
            try:
                value = value_template.async_render(variables)
            except TemplateError as ex:
                raise ConditionErrorMessage(
                    "numeric_state", f"template error: {ex}"
                ) from ex

        # Known states or attribute values that never match the numeric condition
        if value in (None, Const.STATE_UNAVAILABLE, Const.STATE_UNKNOWN):
            Trace.set_condition_result(
                False,
                message=f"value '{value}' is non-numeric and treated as False",
            )
            return False

        try:
            fvalue = float(value)
        except (ValueError, TypeError) as ex:
            raise ConditionErrorMessage(
                "numeric_state",
                f"entity {entity_id} state '{value}' cannot be processed as a number",
            ) from ex

        if below is not None:
            if isinstance(below, str):
                if not (below_entity := self._shc.states.get(below)):
                    raise ConditionErrorMessage(
                        "numeric_state", f"unknown 'below' entity {below}"
                    )
                if below_entity.state in (
                    Const.STATE_UNAVAILABLE,
                    Const.STATE_UNKNOWN,
                ):
                    return False
                try:
                    if fvalue >= float(below_entity.state):
                        Trace.set_condition_result(
                            False,
                            state=fvalue,
                            wanted_state_below=float(below_entity.state),
                        )
                        return False
                except (ValueError, TypeError) as ex:
                    raise ConditionErrorMessage(
                        "numeric_state",
                        f"the 'below' entity {below} state '{below_entity.state}' "
                        + "cannot be processed as a number",
                    ) from ex
            elif fvalue >= below:
                Trace.set_condition_result(
                    False, state=fvalue, wanted_state_below=below
                )
                return False

        if above is not None:
            if isinstance(above, str):
                if not (above_entity := self._shc.states.get(above)):
                    raise ConditionErrorMessage(
                        "numeric_state", f"unknown 'above' entity {above}"
                    )
                if above_entity.state in (
                    Const.STATE_UNAVAILABLE,
                    Const.STATE_UNKNOWN,
                ):
                    return False
                try:
                    if fvalue <= float(above_entity.state):
                        Trace.set_condition_result(
                            False,
                            state=fvalue,
                            wanted_state_above=float(above_entity.state),
                        )
                        return False
                except (ValueError, TypeError) as ex:
                    raise ConditionErrorMessage(
                        "numeric_state",
                        f"the 'above' entity {above} state '{above_entity.state}' cannot "
                        + "be processed as a number",
                    ) from ex
            elif fvalue <= above:
                Trace.set_condition_result(
                    False, state=fvalue, wanted_state_above=above
                )
                return False

        Trace.set_condition_result(True, state=fvalue)
        return True

    def async_numeric_state_from_config(
        self, config: ConfigType
    ) -> ConditionCheckerType:
        """Wrap action method with state based condition."""
        entity_ids = (config.get(Const.CONF_ENTITY_ID, []),)
        attribute = config.get(Const.CONF_ATTRIBUTE)
        below = config.get(Const.CONF_BELOW)
        above = config.get(Const.CONF_ABOVE)
        value_template = config.get(Const.CONF_VALUE_TEMPLATE)

        @Trace.condition_function
        def if_numeric_state(variables: TemplateVarsType = None) -> bool:
            """Test numeric state condition."""
            if value_template is not None:
                value_template.shc = self._shc

            errors = []
            for index, entity_id in enumerate(entity_ids):
                try:
                    with Trace.path(["entity_id", str(index)]), Trace.condition(
                        variables
                    ):
                        if not self.async_numeric_state(
                            entity_id,
                            below,
                            above,
                            value_template,
                            variables,
                            attribute,
                        ):
                            return False
                except ConditionError as ex:
                    errors.append(
                        ConditionErrorIndex(
                            "numeric_state",
                            index=index,
                            total=len(entity_ids),
                            error=ex,
                        )
                    )

            # Raise the errors if no check was false
            if errors:
                raise ConditionErrorContainer("numeric_state", errors=errors)

            return True

        return if_numeric_state

    def state(
        self,
        entity: str | State,
        req_state: typing.Any,
        for_period: datetime.timedelta = None,
        attribute: str = None,
    ) -> bool:
        """Test if state matches requirements.

        Async friendly.
        """
        if entity is None:
            raise ConditionErrorMessage("state", "no entity specified")

        if isinstance(entity, str):
            entity_id = entity

            if (entity := self._shc.states.get(entity)) is None:
                raise ConditionErrorMessage("state", f"unknown entity {entity_id}")
        else:
            entity_id = entity.entity_id

        if attribute is not None and attribute not in entity.attributes:
            Trace.set_condition_result(
                False,
                message=f"attribute '{attribute}' of entity {entity_id} does not exist",
            )
            return False

        assert isinstance(entity, State)

        if attribute is None:
            value: typing.Any = entity.state
        else:
            value = entity.attributes.get(attribute)

        if not isinstance(req_state, list):
            req_state = [req_state]

        is_state = False
        for req_state_value in req_state:
            state_value = req_state_value
            if (
                isinstance(req_state_value, str)
                and _INPUT_ENTITY_ID.match(req_state_value) is not None
            ):
                if not (state_entity := self._shc.states.get(req_state_value)):
                    raise ConditionErrorMessage(
                        "state", f"the 'state' entity {req_state_value} is unavailable"
                    )
                state_value = state_entity.state
            is_state = value == state_value
            if is_state:
                break

        if for_period is None or not is_state:
            Trace.set_condition_result(is_state, state=value, wanted_state=state_value)
            return is_state

        duration = helpers.utcnow() - for_period
        duration_ok = duration > entity.last_changed
        Trace.set_condition_result(duration_ok, state=value, duration=duration)
        return duration_ok

    def state_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Wrap action method with state based condition."""
        entity_ids = config.get(Const.CONF_ENTITY_ID, [])
        req_states: str | list[str] = config.get(Const.CONF_STATE, [])
        for_period = config.get("for")
        attribute = config.get(Const.CONF_ATTRIBUTE)
        match = config.get(Const.CONF_MATCH, Const.ENTITY_MATCH_ALL)

        if not isinstance(req_states, list):
            req_states = [req_states]

        @Trace.condition_function
        def if_state(variables: TemplateVarsType = None) -> bool:
            """Test if condition."""
            errors = []
            result: bool = match != Const.ENTITY_MATCH_ANY
            for index, entity_id in enumerate(entity_ids):
                try:
                    with Trace.path(["entity_id", str(index)]), Trace.condition(
                        variables
                    ):
                        if self.state(entity_id, req_states, for_period, attribute):
                            result = True
                        elif match == Const.ENTITY_MATCH_ALL:
                            return False
                except ConditionError as ex:
                    errors.append(
                        ConditionErrorIndex(
                            "state", index=index, total=len(entity_ids), error=ex
                        )
                    )

            # Raise the errors if no check was false
            if errors:
                raise ConditionErrorContainer("state", errors=errors)

            return result

        return if_state

    def sun(
        self,
        before: str = None,
        after: str = None,
        before_offset: datetime.timedelta = None,
        after_offset: datetime.timedelta = None,
    ) -> bool:
        """Test if current time matches sun requirements."""
        utcnow = helpers.utcnow()
        today = helpers.as_local(utcnow).date()
        before_offset = before_offset or datetime.timedelta(0)
        after_offset = after_offset or datetime.timedelta(0)

        sunrise_today = Sun.get_astral_event_date(Const.SUN_EVENT_SUNRISE, today)
        sunset_today = Sun.get_astral_event_date(Const.SUN_EVENT_SUNSET, today)

        sunrise = sunrise_today
        sunset = sunset_today
        if today > helpers.as_local(
            typing.cast(datetime, sunrise_today)
        ).date() and Const.SUN_EVENT_SUNRISE in (before, after):
            tomorrow = helpers.as_local(utcnow + datetime.timedelta(days=1)).date()
            sunrise_tomorrow = Sun.get_astral_event_date(
                Const.SUN_EVENT_SUNRISE, tomorrow
            )
            sunrise = sunrise_tomorrow

        if today > helpers.as_local(
            typing.cast(datetime, sunset_today)
        ).date() and Const.SUN_EVENT_SUNSET in (before, after):
            tomorrow = helpers.as_local(utcnow + datetime.timedelta(days=1)).date()
            sunset_tomorrow = Sun.get_astral_event_date(
                Const.SUN_EVENT_SUNSET, tomorrow
            )
            sunset = sunset_tomorrow

        if sunrise is None and Const.SUN_EVENT_SUNRISE in (before, after):
            # There is no sunrise today
            Trace.set_condition_result(False, message="no sunrise today")
            return False

        if sunset is None and Const.SUN_EVENT_SUNSET in (before, after):
            # There is no sunset today
            Trace.set_condition_result(False, message="no sunset today")
            return False

        if before == Const.SUN_EVENT_SUNRISE:
            wanted_time_before = typing.cast(datetime, sunrise) + before_offset
            Trace.update_result(wanted_time_before=wanted_time_before)
            if utcnow > wanted_time_before:
                return False

        if before == Const.SUN_EVENT_SUNSET:
            wanted_time_before = typing.cast(datetime, sunset) + before_offset
            Trace.update_result(wanted_time_before=wanted_time_before)
            if utcnow > wanted_time_before:
                return False

        if after == Const.SUN_EVENT_SUNRISE:
            wanted_time_after = typing.cast(datetime, sunrise) + after_offset
            Trace.update_result(wanted_time_after=wanted_time_after)
            if utcnow < wanted_time_after:
                return False

        if after == Const.SUN_EVENT_SUNSET:
            wanted_time_after = typing.cast(datetime, sunset) + after_offset
            Trace.update_result(wanted_time_after=wanted_time_after)
            if utcnow < wanted_time_after:
                return False

        return True

    def sun_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Wrap action method with sun based condition."""
        before = config.get("before")
        after = config.get("after")
        before_offset = config.get("before_offset")
        after_offset = config.get("after_offset")

        @Trace.condition_function
        def sun_if(_variables: TemplateVarsType = None) -> bool:
            """Validate time based if-condition."""
            return self.sun(before, after, before_offset, after_offset)

        return sun_if

    @staticmethod
    def template(
        shc: SmartHomeController,
        value_template: Template,
        variables: TemplateVarsType = None,
    ) -> bool:
        """Test if template condition matches."""
        return shc.run_callback_threadsafe(
            ScriptCondition.async_template, shc, value_template, variables
        ).result()

    @staticmethod
    def async_template(
        value_template: Template,
        variables: TemplateVarsType = None,
        trace_result: bool = True,
    ) -> bool:
        """Test if template condition matches."""
        try:
            info = value_template.async_render_to_info(variables, parse_result=False)
            value = info.result()
        except TemplateError as ex:
            raise ConditionErrorMessage("template", str(ex)) from ex

        result = value.lower() == "true"
        if trace_result:
            Trace.set_condition_result(result, entities=list(info.entities))
        return result

    def async_template_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Wrap action method with state based condition."""
        value_template = typing.cast(Template, config.get(Const.CONF_VALUE_TEMPLATE))

        @Trace.condition_function
        def template_if(variables: TemplateVarsType = None) -> bool:
            """Validate template based if-condition."""
            value_template.shc = self._shc

            return self.async_template(value_template, variables)

        return template_if

    def time(
        self,
        before: datetime.time | str = None,
        after: datetime.time | str = None,
        weekday: str | collections.abc.Container[str] = None,
    ) -> bool:
        """Test if local time condition matches.

        Handle the fact that time is continuous and we may be testing for
        a period that crosses midnight. In that case it is easier to test
        for the opposite. "(23:59 <= now < 00:01)" would be the same as
        "not (00:01 <= now < 23:59)".
        """
        now = helpers.now()
        now_time = now.time()

        if after is None:
            after = datetime.time(0)
        elif isinstance(after, str):
            if not (after_entity := self._shc.states.get(after)):
                raise ConditionErrorMessage("time", f"unknown 'after' entity {after}")
            if after_entity.domain == "input_datetime":
                after = datetime.time(
                    after_entity.attributes.get("hour", 23),
                    after_entity.attributes.get("minute", 59),
                    after_entity.attributes.get("second", 59),
                )
            elif after_entity.attributes.get(
                Const.ATTR_DEVICE_CLASS
            ) == Sensor.DeviceClass.TIMESTAMP and after_entity.state not in (
                Const.STATE_UNAVAILABLE,
                Const.STATE_UNKNOWN,
            ):
                after_datetime = helpers.parse_datetime(after_entity.state)
                if after_datetime is None:
                    return False
                after = helpers.as_local(after_datetime).time()
            else:
                return False

        if before is None:
            before = datetime.time(23, 59, 59, 999999)
        elif isinstance(before, str):
            if not (before_entity := self._shc.states.get(before)):
                raise ConditionErrorMessage("time", f"unknown 'before' entity {before}")
            if before_entity.domain == "input_datetime":
                before = datetime.time(
                    before_entity.attributes.get("hour", 23),
                    before_entity.attributes.get("minute", 59),
                    before_entity.attributes.get("second", 59),
                )
            elif before_entity.attributes.get(
                Const.ATTR_DEVICE_CLASS
            ) == Sensor.DeviceClass.TIMESTAMP and before_entity.state not in (
                Const.STATE_UNAVAILABLE,
                Const.STATE_UNKNOWN,
            ):
                before_timedatime = helpers.parse_datetime(before_entity.state)
                if before_timedatime is None:
                    return False
                before = helpers.as_local(before_timedatime).time()
            else:
                return False

        if after < before:
            Trace.update_result(after=after, now_time=now_time, before=before)
            if not after <= now_time < before:
                return False
        else:
            Trace.update_result(after=after, now_time=now_time, before=before)
            if before <= now_time < after:
                return False

        if weekday is not None:
            now_weekday = Const.WEEKDAYS[now.weekday()]

            Trace.update_result(weekday=weekday, now_weekday=now_weekday)
            if (
                isinstance(weekday, str)
                and weekday != now_weekday
                or now_weekday not in weekday
            ):
                return False

        return True

    def time_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Wrap action method with time based condition."""
        before = config.get(Const.CONF_BEFORE)
        after = config.get(Const.CONF_AFTER)
        weekday = config.get(Const.CONF_WEEKDAY)

        @Trace.condition_function
        def time_if(_variables: TemplateVarsType = None) -> bool:
            """Validate time based if-condition."""
            return self.time(before, after, weekday)

        return time_if

    def zone(
        self,
        zone_ent: str | State,
        entity: str | State,
    ) -> bool:
        """Test if zone-condition matches.

        Async friendly.
        """
        if zone_ent is None:
            raise ConditionErrorMessage("zone", "no zone specified")

        if isinstance(zone_ent, str):
            zone_ent_id = zone_ent

            if (zone_ent := self._shc.states.get(zone_ent)) is None:
                raise ConditionErrorMessage("zone", f"unknown zone {zone_ent_id}")

        if entity is None:
            raise ConditionErrorMessage("zone", "no entity specified")

        if isinstance(entity, str):
            entity_id = entity

            if (entity := self._shc.states.get(entity)) is None:
                raise ConditionErrorMessage("zone", f"unknown entity {entity_id}")
        else:
            entity_id = entity.entity_id

        if entity.state in (
            Const.STATE_UNAVAILABLE,
            Const.STATE_UNKNOWN,
        ):
            return False

        latitude = entity.attributes.get(Const.ATTR_LATITUDE)
        longitude = entity.attributes.get(Const.ATTR_LONGITUDE)

        if latitude is None:
            raise ConditionErrorMessage(
                "zone", f"entity {entity_id} has no 'latitude' attribute"
            )

        if longitude is None:
            raise ConditionErrorMessage(
                "zone", f"entity {entity_id} has no 'longitude' attribute"
            )

        return LocationInfo.in_zone(
            zone_ent,
            latitude,
            longitude,
            entity.attributes.get(Const.ATTR_GPS_ACCURACY, 0),
        )

    def zone_from_config(self, config: ConfigType) -> ConditionCheckerType:
        """Wrap action method with zone based condition."""
        entity_ids = config.get(Const.CONF_ENTITY_ID, [])
        zone_entity_ids = config.get(Const.CONF_ZONE, [])

        @Trace.condition_function
        def if_in_zone(_variables: TemplateVarsType = None) -> bool:
            """Test if condition."""
            errors = []

            all_ok = True
            for entity_id in entity_ids:
                entity_ok = False
                for zone_entity_id in zone_entity_ids:
                    try:
                        if self.zone(zone_entity_id, entity_id):
                            entity_ok = True
                    except ConditionErrorMessage as ex:
                        errors.append(
                            ConditionErrorMessage(
                                "zone",
                                f"error matching {entity_id} with {zone_entity_id}: {ex.message}",
                            )
                        )

                if not entity_ok:
                    all_ok = False

            # Raise the errors only if no definitive result was found
            if errors and not all_ok:
                raise ConditionErrorContainer("zone", errors=errors)

            return all_ok

        return if_in_zone

    async def async_device_from_config(
        self, config: ConfigType
    ) -> ConditionCheckerType:
        """Test a device condition."""
        platform = await _async_get_device_automation_platform(
            self._shc, config[Const.CONF_DOMAIN]
        )
        return await platform.async_condition_from_config(config)

    async def async_validate_device_condition_config(
        self, config: ConfigType
    ) -> ConfigType:
        platform = await _async_get_device_automation_platform(
            self._shc, config[Const.CONF_DOMAIN]
        )
        schema = platform.condition_schema
        if schema is not None:
            return schema(config)
        return await platform.async_validate_condition_config(config)

    async def async_trigger_from_config(config: ConfigType) -> ConditionCheckerType:
        """Test a trigger condition."""
        trigger_id = config[Const.CONF_ID]

        @Trace.condition_function
        def trigger_if(variables: TemplateVarsType = None) -> bool:
            """Validate trigger based if-condition."""
            return (
                variables is not None
                and "trigger" in variables
                and variables["trigger"].get("id") in trigger_id
            )

        return trigger_if

    def numeric_state_validate_config(self, config: ConfigType) -> ConfigType:
        """Validate numeric_state condition config."""

        registry = self._shc.entity_registry
        config = dict(config)
        config[Const.CONF_ENTITY_ID] = registry.async_validate_entity_ids(
            cv.entity_ids_or_uuids(config[Const.CONF_ENTITY_ID])
        )
        return config

    def state_validate_config(self, config: ConfigType) -> ConfigType:
        """Validate state condition config."""

        registry = self._shc.entity_registry
        config = dict(config)
        config[Const.CONF_ENTITY_ID] = registry.async_validate_entity_ids(
            cv.entity_ids_or_uuids(config[Const.CONF_ENTITY_ID])
        )
        return config

    async def async_validate_condition_config(self, config: ConfigType) -> ConfigType:
        """Validate config."""
        condition = config[Const.CONF_CONDITION]
        if condition in ("and", "not", "or"):
            conditions = []
            for sub_cond in config["conditions"]:
                sub_cond = await self.async_validate_condition_config(sub_cond)
                conditions.append(sub_cond)
            config["conditions"] = conditions
            return config

        if condition == "device":
            return await self.async_validate_device_condition_config(config)

        if condition in ("numeric_state", "state"):
            if condition == "state":
                return self.state_validate_config(config)
            return self.numeric_state_validate_config(config)

        return config

    @staticmethod
    async def async_validate_conditions_config(
        shc: SmartHomeController, conditions: list[ConfigType]
    ) -> list[ConfigType | Template]:
        """Validate config."""
        cond_prot = ScriptCondition.get_action_condition_protocol(shc)
        return await asyncio.gather(
            *(cond_prot.async_validate_condition_config(cond) for cond in conditions)
        )

    @staticmethod
    async def async_validate_automation_condition_config(
        shc: SmartHomeController, config: ConfigType
    ) -> ConfigType:
        """Validate config."""
        cond_prot = ScriptCondition.get_action_condition_protocol(shc)
        return await cond_prot.async_validate_condition_config(config)

    @staticmethod
    @callback
    def async_extract_entities(config: ConfigType | Template) -> set[str]:
        """Extract entities from a condition."""
        referenced: set[str] = set()
        to_process = collections.deque([config])

        while to_process:
            config = to_process.popleft()
            if isinstance(config, Template):
                continue

            condition = config[Const.CONF_CONDITION]

            if condition in ("and", "not", "or"):
                to_process.extend(config["conditions"])
                continue

            entity_ids = config.get(Const.CONF_ENTITY_ID)

            if isinstance(entity_ids, str):
                entity_ids = [entity_ids]

            if entity_ids is not None:
                referenced.update(entity_ids)

        return referenced

    @staticmethod
    @callback
    def async_extract_devices(config: ConfigType | Template) -> set[str]:
        """Extract devices from a condition."""
        referenced = set()
        to_process = collections.deque([config])

        while to_process:
            config = to_process.popleft()
            if isinstance(config, Template):
                continue

            condition = config[Const.CONF_CONDITION]

            if condition in ("and", "not", "or"):
                to_process.extend(config["conditions"])
                continue

            if condition != "device":
                continue

            if (device_id := config.get(Const.CONF_DEVICE_ID)) is not None:
                referenced.add(device_id)

        return referenced


async def _async_get_device_automation_platform(
    shc: SmartHomeController, domain: str
) -> ActionConditionPlatform:
    """
    Get the device automation platform for Action, ActionCondition
    or Trigger.
    """
    await shc.setup.async_get_integration_with_requirements(domain)
    comp = SmartHomeControllerComponent.get_component(domain)
    if not isinstance(comp, SmartHomeControllerComponent):
        raise InvalidDeviceAutomationConfig(f"Component '{domain}' not found.")
    result = comp.get_platform(Platform.CONDITION)
    if not isinstance(result, ActionConditionPlatform):
        raise InvalidDeviceAutomationConfig(
            f"Action Condition Platform in domain '{domain}' not found."
        )
    return result
