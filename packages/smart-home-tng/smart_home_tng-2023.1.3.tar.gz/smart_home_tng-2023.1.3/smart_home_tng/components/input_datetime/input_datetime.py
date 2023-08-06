"""
Input Datetime Component for Smart Home - The Next Generation.

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

import datetime

import voluptuous as vol

from ... import core
from .const import Const


# pylint: disable=unused-variable
class InputDatetime(core.RestoreEntity):
    """Representation of a datetime input."""

    _domain: str

    def __init__(self, config: dict) -> None:
        """Initialize a select input."""
        self._config = config
        self._editable = True
        self._current_datetime = None

        if not (initial := config.get(Const.CONF_INITIAL)):
            return

        if self.has_date and self.has_time:
            current_datetime = core.helpers.parse_datetime(initial)

        elif self.has_date:
            date = core.helpers.parse_date(initial)
            current_datetime = datetime.datetime.combine(date, Const.DEFAULT_TIME)

        else:
            time = core.helpers.parse_time(initial)
            current_datetime = datetime.datetime.combine(datetime.date.today(), time)

        # If the user passed in an initial value with a timezone, convert it to right tz
        if current_datetime.tzinfo is not None:
            self._current_datetime = current_datetime.astimezone(
                core.helpers.get_default_time_zone()
            )
        else:
            self._current_datetime = current_datetime.replace(
                tzinfo=core.helpers.get_default_time_zone
            )

    @property
    def editable(self) -> bool:
        return self._editable

    @classmethod
    def from_yaml(cls, config: dict):
        """Return entity instance initialized from yaml storage."""
        input_dt = cls(config)
        input_dt.entity_id = f"{InputDatetime._domain}.{config[core.Const.CONF_ID]}"
        input_dt._editable = False
        return input_dt

    async def async_added_to_shc(self):
        """Run when entity about to be added."""
        await super().async_added_to_shc()

        # Priority 1: Initial value
        if self.state is not None:
            return

        default_value = datetime.datetime.today().strftime("%Y-%m-%d 00:00:00")

        # Priority 2: Old state
        if (old_state := await self.async_get_last_state()) is None:
            self._current_datetime = core.helpers.parse_datetime(default_value)
            return

        if self.has_date and self.has_time:
            date_time = core.helpers.parse_datetime(old_state.state)
            if date_time is None:
                current_datetime = core.helpers.parse_datetime(default_value)
            else:
                current_datetime = date_time

        elif self.has_date:
            if (date := core.helpers.parse_date(old_state.state)) is None:
                current_datetime = core.helpers.parse_datetime(default_value)
            else:
                current_datetime = datetime.datetime.combine(date, Const.DEFAULT_TIME)

        else:
            if (time := core.helpers.parse_time(old_state.state)) is None:
                current_datetime = core.helpers.parse_datetime(default_value)
            else:
                current_datetime = datetime.datetime.combine(
                    datetime.date.today(), time
                )

        self._current_datetime = current_datetime.replace(
            tzinfo=core.helpers.get_default_time_zone()
        )

    @property
    def should_poll(self):
        """If entity should be polled."""
        return False

    @property
    def name(self):
        """Return the name of the select input."""
        return self._config.get(core.Const.CONF_NAME)

    @property
    def has_date(self) -> bool:
        """Return True if entity has date."""
        return self._config[Const.CONF_HAS_DATE]

    @property
    def has_time(self) -> bool:
        """Return True if entity has time."""
        return self._config[Const.CONF_HAS_TIME]

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return self._config.get(core.Const.CONF_ICON)

    @property
    def state(self):
        """Return the state of the component."""
        if self._current_datetime is None:
            return None

        if self.has_date and self.has_time:
            return self._current_datetime.strftime(Const.FMT_DATETIME)

        if self.has_date:
            return self._current_datetime.strftime(Const.FMT_DATE)

        return self._current_datetime.strftime(Const.FMT_TIME)

    @property
    def capability_attributes(self) -> dict:
        """Return the capability attributes."""
        return {
            Const.CONF_HAS_DATE: self.has_date,
            Const.CONF_HAS_TIME: self.has_time,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            core.Const.ATTR_EDITABLE: self.editable,
        }

        if self._current_datetime is None:
            return attrs

        if self.has_date and self._current_datetime is not None:
            attrs["year"] = self._current_datetime.year
            attrs["month"] = self._current_datetime.month
            attrs["day"] = self._current_datetime.day

        if self.has_time and self._current_datetime is not None:
            attrs["hour"] = self._current_datetime.hour
            attrs["minute"] = self._current_datetime.minute
            attrs["second"] = self._current_datetime.second

        if not self.has_date:
            attrs["timestamp"] = (
                self._current_datetime.hour * 3600
                + self._current_datetime.minute * 60
                + self._current_datetime.second
            )

        elif not self.has_time:
            extended = datetime.datetime.combine(
                self._current_datetime, datetime.time(0, 0)
            )
            attrs["timestamp"] = extended.timestamp()

        else:
            attrs["timestamp"] = self._current_datetime.timestamp()

        return attrs

    @property
    def unique_id(self) -> str:
        """Return unique id of the entity."""
        return self._config[core.Const.CONF_ID]

    @core.callback
    def async_set_datetime(self, date=None, time=None, date_time=None, timestamp=None):
        """Set a new date / time."""
        if timestamp:
            date_time = core.helpers.as_local(core.Const.utc_from_timestamp(timestamp))

        if date_time:
            date = date_time.date()
            time = date_time.time()

        if not self.has_date:
            date = None

        if not self.has_time:
            time = None

        if not date and not time:
            raise vol.Invalid("Nothing to set")

        if not date:
            date = self._current_datetime.date()

        if not time:
            time = self._current_datetime.time()

        self._current_datetime = datetime.datetime.combine(
            date, time, core.helpers.get_default_time_zone
        )
        self.async_write_state()

    async def async_update_config(self, config: dict) -> None:
        """Handle when the config is updated."""
        self._config = config
        self.async_write_state()
