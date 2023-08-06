"""
Helpers for Components of Smart Home - The Next Generation.

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

from ..selector import _SELECTORS
from ..action_selector import ActionSelector
from ..addon_selector import AddonSelector
from ..area_selector import AreaSelector
from ..attribute_selector import AttributeSelector
from ..boolean_selector import BooleanSelector
from ..color_rgb_selector import ColorRGBSelector
from ..color_temp_selector import ColorTempSelector
from ..date_selector import DateSelector
from ..device_selector import DeviceSelector
from ..duration_selector import DurationSelector
from ..entity_selector import EntitySelector
from ..icon_selector import IconSelector
from ..location_selector import LocationSelector
from ..media_selector import MediaSelector
from ..number_selector import NumberSelector
from ..object_selector import ObjectSelector
from ..select_selector import SelectSelector
from ..target_selector import TargetSelector
from ..template_selector import TemplateSelector
from ..text_selector import TextSelector
from ..theme_selector import ThemeSelector
from ..time_selector import TimeSelector


# pylint: disable=unused-variable
def register_selectors():
    """
    Reqister selector class manual, because 'Registry' requires
    any function call to module, before 'Auto-Registration' is
    triggered.
    """
    _SELECTORS["action"] = ActionSelector
    _SELECTORS["addon"] = AddonSelector
    _SELECTORS["area"] = AreaSelector
    _SELECTORS["attribute"] = AttributeSelector
    _SELECTORS["boolean"] = BooleanSelector
    _SELECTORS["color_rgb"] = ColorRGBSelector
    _SELECTORS["color_temp"] = ColorTempSelector
    _SELECTORS["date"] = DateSelector
    _SELECTORS["device"] = DeviceSelector
    _SELECTORS["duration"] = DurationSelector
    _SELECTORS["entity"] = EntitySelector
    _SELECTORS["icon"] = IconSelector
    _SELECTORS["location"] = LocationSelector
    _SELECTORS["media"] = MediaSelector
    _SELECTORS["number"] = NumberSelector
    _SELECTORS["object"] = ObjectSelector
    _SELECTORS["select"] = SelectSelector
    _SELECTORS["target"] = TargetSelector
    _SELECTORS["template"] = TemplateSelector
    _SELECTORS["text"] = TextSelector
    _SELECTORS["theme"] = ThemeSelector
    _SELECTORS["time"] = TimeSelector
