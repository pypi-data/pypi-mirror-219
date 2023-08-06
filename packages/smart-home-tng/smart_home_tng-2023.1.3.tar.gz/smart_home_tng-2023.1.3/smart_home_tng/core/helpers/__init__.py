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

# pylint: disable=unused-variable

from .asyncio import (
    block_async_io,
    check_loop,
    fire_coroutine_threadsafe,
    gather_with_concurrency,
    protect_loop,
    run_callback_threadsafe,
    shutdown_run_callback_threadsafe,
)
from .color import Color
from .config_validation import boolean, positive_int, string
from .core import (
    async_generate_entity_id,
    convert,
    ensure_unique_string,
    get_random_string,
    raise_if_invalid_filename,
    raise_if_invalid_path,
    repr_helper,
    slugify,
    split_entity_id,
    valid_entity_id,
)
from .device_registry import format_mac
from .dt import (
    as_local,
    as_timestamp,
    as_utc,
    find_next_time_expression_time,
    get_age,
    get_default_time_zone,
    get_time_zone,
    now,
    parse_date,
    parse_datetime,
    parse_duration,
    parse_time,
    parse_time_expression,
    set_default_time_zone,
    start_of_local_day,
    utc_from_timestamp,
    utc_to_timestamp,
    utcnow,
)
from .file import write_utf8_file, write_utf8_file_atomic
from .icon import icon_for_battery_level, icon_for_signal_level
from .integration import get_integration_frame, report, report_integration, warn_use
from .json import (
    find_paths_unserializable_data,
    format_unserializable_data,
    json_loads,
    load_json,
    save_json,
)
from .logging import (
    async_create_catching_coro,
    catch_log_coro_exception,
    catch_log_exception,
    log_exception,
)
from .network import (
    is_invalid,
    is_ip_address,
    is_ipv4_address,
    is_ipv6_address,
    is_link_local,
    is_local,
    is_loopback,
    is_private,
    normalize_url,
)
from .percentage import (
    int_states_in_range,
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
    percentage_to_ranged_value,
    ranged_value_to_percentage,
    states_in_range,
)
from .state import async_reproduce_state, async_reproduce_states
from .system_info import async_get_system_info
from .temperature import display_temp
from .ulid import ulid, ulid_hex
from .uuid import random_uuid_hex
from .webhook import serialize_response
from .yaml import dump, represent_odict, save_yaml
