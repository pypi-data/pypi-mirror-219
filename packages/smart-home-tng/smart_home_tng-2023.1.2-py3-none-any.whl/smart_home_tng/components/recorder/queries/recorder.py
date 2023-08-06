"""
Recorder Component for Smart Home - The Next Generation.

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

import collections.abc
import datetime as dt

import sqlalchemy as sql

from .. import model
from ..const import Const

# pylint: disable=unused-variable


def find_shared_attributes_id(
    data_hash: int, shared_attrs: str
) -> sql.sql.StatementLambdaElement:
    """Find an attributes_id by hash and shared_attrs."""
    return sql.lambda_stmt(
        lambda: sql.select(model.StateAttributes.attributes_id)
        .filter(model.StateAttributes.hash == data_hash)
        .filter(model.StateAttributes.shared_attrs == shared_attrs)
    )


def find_shared_data_id(
    attr_hash: int, shared_data: str
) -> sql.sql.StatementLambdaElement:
    """Find a data_id by hash and shared_data."""
    return sql.lambda_stmt(
        lambda: sql.select(model.EventData.data_id)
        .filter(model.EventData.hash == attr_hash)
        .filter(model.EventData.shared_data == shared_data)
    )


def _state_attrs_exist(attr: int) -> sql.sql.Select:
    """Check if a state attributes id exists in the states table."""
    return sql.select(sql.func.min(model.States.attributes_id)).where(
        model.States.attributes_id == attr
    )


def attributes_ids_exist_in_states_sqlite(
    attributes_ids: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Find attributes ids that exist in the states table."""
    return sql.lambda_stmt(
        lambda: sql.select(sql.distinct(model.States.attributes_id)).filter(
            model.States.attributes_id.in_(attributes_ids)
        )
    )


def attributes_ids_exist_in_states(
    attr1: int,
    attr2: int,
    attr3: int,
    attr4: int,
    attr5: int,
    attr6: int,
    attr7: int,
    attr8: int,
    attr9: int,
    attr10: int,
    attr11: int,
    attr12: int,
    attr13: int,
    attr14: int,
    attr15: int,
    attr16: int,
    attr17: int,
    attr18: int,
    attr19: int,
    attr20: int,
    attr21: int,
    attr22: int,
    attr23: int,
    attr24: int,
    attr25: int,
    attr26: int,
    attr27: int,
    attr28: int,
    attr29: int,
    attr30: int,
    attr31: int,
    attr32: int,
    attr33: int,
    attr34: int,
    attr35: int,
    attr36: int,
    attr37: int,
    attr38: int,
    attr39: int,
    attr40: int,
    attr41: int,
    attr42: int,
    attr43: int,
    attr44: int,
    attr45: int,
    attr46: int,
    attr47: int,
    attr48: int,
    attr49: int,
    attr50: int,
    attr51: int,
    attr52: int,
    attr53: int,
    attr54: int,
    attr55: int,
    attr56: int,
    attr57: int,
    attr58: int,
    attr59: int,
    attr60: int,
    attr61: int,
    attr62: int,
    attr63: int,
    attr64: int,
    attr65: int,
    attr66: int,
    attr67: int,
    attr68: int,
    attr69: int,
    attr70: int,
    attr71: int,
    attr72: int,
    attr73: int,
    attr74: int,
    attr75: int,
    attr76: int,
    attr77: int,
    attr78: int,
    attr79: int,
    attr80: int,
    attr81: int,
    attr82: int,
    attr83: int,
    attr84: int,
    attr85: int,
    attr86: int,
    attr87: int,
    attr88: int,
    attr89: int,
    attr90: int,
    attr91: int,
    attr92: int,
    attr93: int,
    attr94: int,
    attr95: int,
    attr96: int,
    attr97: int,
    attr98: int,
    attr99: int,
    attr100: int,
) -> sql.sql.StatementLambdaElement:
    """Generate the find attributes select only once.

    https://docs.sqlalchemy.org/en/14/core/connections.html#quick-guidelines-for-lambdas
    """
    return sql.lambda_stmt(
        lambda: sql.union_all(
            _state_attrs_exist(attr1),
            _state_attrs_exist(attr2),
            _state_attrs_exist(attr3),
            _state_attrs_exist(attr4),
            _state_attrs_exist(attr5),
            _state_attrs_exist(attr6),
            _state_attrs_exist(attr7),
            _state_attrs_exist(attr8),
            _state_attrs_exist(attr9),
            _state_attrs_exist(attr10),
            _state_attrs_exist(attr11),
            _state_attrs_exist(attr12),
            _state_attrs_exist(attr13),
            _state_attrs_exist(attr14),
            _state_attrs_exist(attr15),
            _state_attrs_exist(attr16),
            _state_attrs_exist(attr17),
            _state_attrs_exist(attr18),
            _state_attrs_exist(attr19),
            _state_attrs_exist(attr20),
            _state_attrs_exist(attr21),
            _state_attrs_exist(attr22),
            _state_attrs_exist(attr23),
            _state_attrs_exist(attr24),
            _state_attrs_exist(attr25),
            _state_attrs_exist(attr26),
            _state_attrs_exist(attr27),
            _state_attrs_exist(attr28),
            _state_attrs_exist(attr29),
            _state_attrs_exist(attr30),
            _state_attrs_exist(attr31),
            _state_attrs_exist(attr32),
            _state_attrs_exist(attr33),
            _state_attrs_exist(attr34),
            _state_attrs_exist(attr35),
            _state_attrs_exist(attr36),
            _state_attrs_exist(attr37),
            _state_attrs_exist(attr38),
            _state_attrs_exist(attr39),
            _state_attrs_exist(attr40),
            _state_attrs_exist(attr41),
            _state_attrs_exist(attr42),
            _state_attrs_exist(attr43),
            _state_attrs_exist(attr44),
            _state_attrs_exist(attr45),
            _state_attrs_exist(attr46),
            _state_attrs_exist(attr47),
            _state_attrs_exist(attr48),
            _state_attrs_exist(attr49),
            _state_attrs_exist(attr50),
            _state_attrs_exist(attr51),
            _state_attrs_exist(attr52),
            _state_attrs_exist(attr53),
            _state_attrs_exist(attr54),
            _state_attrs_exist(attr55),
            _state_attrs_exist(attr56),
            _state_attrs_exist(attr57),
            _state_attrs_exist(attr58),
            _state_attrs_exist(attr59),
            _state_attrs_exist(attr60),
            _state_attrs_exist(attr61),
            _state_attrs_exist(attr62),
            _state_attrs_exist(attr63),
            _state_attrs_exist(attr64),
            _state_attrs_exist(attr65),
            _state_attrs_exist(attr66),
            _state_attrs_exist(attr67),
            _state_attrs_exist(attr68),
            _state_attrs_exist(attr69),
            _state_attrs_exist(attr70),
            _state_attrs_exist(attr71),
            _state_attrs_exist(attr72),
            _state_attrs_exist(attr73),
            _state_attrs_exist(attr74),
            _state_attrs_exist(attr75),
            _state_attrs_exist(attr76),
            _state_attrs_exist(attr77),
            _state_attrs_exist(attr78),
            _state_attrs_exist(attr79),
            _state_attrs_exist(attr80),
            _state_attrs_exist(attr81),
            _state_attrs_exist(attr82),
            _state_attrs_exist(attr83),
            _state_attrs_exist(attr84),
            _state_attrs_exist(attr85),
            _state_attrs_exist(attr86),
            _state_attrs_exist(attr87),
            _state_attrs_exist(attr88),
            _state_attrs_exist(attr89),
            _state_attrs_exist(attr90),
            _state_attrs_exist(attr91),
            _state_attrs_exist(attr92),
            _state_attrs_exist(attr93),
            _state_attrs_exist(attr94),
            _state_attrs_exist(attr95),
            _state_attrs_exist(attr96),
            _state_attrs_exist(attr97),
            _state_attrs_exist(attr98),
            _state_attrs_exist(attr99),
            _state_attrs_exist(attr100),
        )
    )


def data_ids_exist_in_events_sqlite(
    data_ids: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Find data ids that exist in the events table."""
    return sql.lambda_stmt(
        lambda: sql.select(sql.distinct(model.Events.data_id)).filter(
            model.Events.data_id.in_(data_ids)
        )
    )


def _event_data_id_exist(data_id: int) -> sql.sql.Select:
    """Check if a event data id exists in the events table."""
    return sql.select(sql.func.min(model.Events.data_id)).where(
        model.Events.data_id == data_id
    )


def data_ids_exist_in_events(
    id1: int,
    id2: int,
    id3: int,
    id4: int,
    id5: int,
    id6: int,
    id7: int,
    id8: int,
    id9: int,
    id10: int,
    id11: int,
    id12: int,
    id13: int,
    id14: int,
    id15: int,
    id16: int,
    id17: int,
    id18: int,
    id19: int,
    id20: int,
    id21: int,
    id22: int,
    id23: int,
    id24: int,
    id25: int,
    id26: int,
    id27: int,
    id28: int,
    id29: int,
    id30: int,
    id31: int,
    id32: int,
    id33: int,
    id34: int,
    id35: int,
    id36: int,
    id37: int,
    id38: int,
    id39: int,
    id40: int,
    id41: int,
    id42: int,
    id43: int,
    id44: int,
    id45: int,
    id46: int,
    id47: int,
    id48: int,
    id49: int,
    id50: int,
    id51: int,
    id52: int,
    id53: int,
    id54: int,
    id55: int,
    id56: int,
    id57: int,
    id58: int,
    id59: int,
    id60: int,
    id61: int,
    id62: int,
    id63: int,
    id64: int,
    id65: int,
    id66: int,
    id67: int,
    id68: int,
    id69: int,
    id70: int,
    id71: int,
    id72: int,
    id73: int,
    id74: int,
    id75: int,
    id76: int,
    id77: int,
    id78: int,
    id79: int,
    id80: int,
    id81: int,
    id82: int,
    id83: int,
    id84: int,
    id85: int,
    id86: int,
    id87: int,
    id88: int,
    id89: int,
    id90: int,
    id91: int,
    id92: int,
    id93: int,
    id94: int,
    id95: int,
    id96: int,
    id97: int,
    id98: int,
    id99: int,
    id100: int,
) -> sql.sql.StatementLambdaElement:
    """Generate the find event data select only once.

    https://docs.sqlalchemy.org/en/14/core/connections.html#quick-guidelines-for-lambdas
    """
    return sql.lambda_stmt(
        lambda: sql.union_all(
            _event_data_id_exist(id1),
            _event_data_id_exist(id2),
            _event_data_id_exist(id3),
            _event_data_id_exist(id4),
            _event_data_id_exist(id5),
            _event_data_id_exist(id6),
            _event_data_id_exist(id7),
            _event_data_id_exist(id8),
            _event_data_id_exist(id9),
            _event_data_id_exist(id10),
            _event_data_id_exist(id11),
            _event_data_id_exist(id12),
            _event_data_id_exist(id13),
            _event_data_id_exist(id14),
            _event_data_id_exist(id15),
            _event_data_id_exist(id16),
            _event_data_id_exist(id17),
            _event_data_id_exist(id18),
            _event_data_id_exist(id19),
            _event_data_id_exist(id20),
            _event_data_id_exist(id21),
            _event_data_id_exist(id22),
            _event_data_id_exist(id23),
            _event_data_id_exist(id24),
            _event_data_id_exist(id25),
            _event_data_id_exist(id26),
            _event_data_id_exist(id27),
            _event_data_id_exist(id28),
            _event_data_id_exist(id29),
            _event_data_id_exist(id30),
            _event_data_id_exist(id31),
            _event_data_id_exist(id32),
            _event_data_id_exist(id33),
            _event_data_id_exist(id34),
            _event_data_id_exist(id35),
            _event_data_id_exist(id36),
            _event_data_id_exist(id37),
            _event_data_id_exist(id38),
            _event_data_id_exist(id39),
            _event_data_id_exist(id40),
            _event_data_id_exist(id41),
            _event_data_id_exist(id42),
            _event_data_id_exist(id43),
            _event_data_id_exist(id44),
            _event_data_id_exist(id45),
            _event_data_id_exist(id46),
            _event_data_id_exist(id47),
            _event_data_id_exist(id48),
            _event_data_id_exist(id49),
            _event_data_id_exist(id50),
            _event_data_id_exist(id51),
            _event_data_id_exist(id52),
            _event_data_id_exist(id53),
            _event_data_id_exist(id54),
            _event_data_id_exist(id55),
            _event_data_id_exist(id56),
            _event_data_id_exist(id57),
            _event_data_id_exist(id58),
            _event_data_id_exist(id59),
            _event_data_id_exist(id60),
            _event_data_id_exist(id61),
            _event_data_id_exist(id62),
            _event_data_id_exist(id63),
            _event_data_id_exist(id64),
            _event_data_id_exist(id65),
            _event_data_id_exist(id66),
            _event_data_id_exist(id67),
            _event_data_id_exist(id68),
            _event_data_id_exist(id69),
            _event_data_id_exist(id70),
            _event_data_id_exist(id71),
            _event_data_id_exist(id72),
            _event_data_id_exist(id73),
            _event_data_id_exist(id74),
            _event_data_id_exist(id75),
            _event_data_id_exist(id76),
            _event_data_id_exist(id77),
            _event_data_id_exist(id78),
            _event_data_id_exist(id79),
            _event_data_id_exist(id80),
            _event_data_id_exist(id81),
            _event_data_id_exist(id82),
            _event_data_id_exist(id83),
            _event_data_id_exist(id84),
            _event_data_id_exist(id85),
            _event_data_id_exist(id86),
            _event_data_id_exist(id87),
            _event_data_id_exist(id88),
            _event_data_id_exist(id89),
            _event_data_id_exist(id90),
            _event_data_id_exist(id91),
            _event_data_id_exist(id92),
            _event_data_id_exist(id93),
            _event_data_id_exist(id94),
            _event_data_id_exist(id95),
            _event_data_id_exist(id96),
            _event_data_id_exist(id97),
            _event_data_id_exist(id98),
            _event_data_id_exist(id99),
            _event_data_id_exist(id100),
        )
    )


def disconnect_states_rows(
    state_ids: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Disconnect states rows."""
    return sql.lambda_stmt(
        lambda: sql.update(model.States)
        .where(model.States.old_state_id.in_(state_ids))
        .values(old_state_id=None)
        .execution_options(synchronize_session=False)
    )


def delete_states_rows(
    state_ids: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Delete states rows."""
    return sql.lambda_stmt(
        lambda: sql.delete(model.States)
        .where(model.States.state_id.in_(state_ids))
        .execution_options(synchronize_session=False)
    )


def delete_event_data_rows(
    data_ids: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Delete event_data rows."""
    return sql.lambda_stmt(
        lambda: sql.delete(model.EventData)
        .where(model.EventData.data_id.in_(data_ids))
        .execution_options(synchronize_session=False)
    )


def delete_states_attributes_rows(
    attributes_ids: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Delete states_attributes rows."""
    return sql.lambda_stmt(
        lambda: sql.delete(model.StateAttributes)
        .where(model.StateAttributes.attributes_id.in_(attributes_ids))
        .execution_options(synchronize_session=False)
    )


def delete_statistics_runs_rows(
    statistics_runs: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Delete statistics_runs rows."""
    return sql.lambda_stmt(
        lambda: sql.delete(model.StatisticsRuns)
        .where(model.StatisticsRuns.run_id.in_(statistics_runs))
        .execution_options(synchronize_session=False)
    )


def delete_statistics_short_term_rows(
    short_term_statistics: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Delete statistics_short_term rows."""
    return sql.lambda_stmt(
        lambda: sql.delete(model.StatisticsShortTerm)
        .where(model.StatisticsShortTerm.id.in_(short_term_statistics))
        .execution_options(synchronize_session=False)
    )


def delete_event_rows(
    event_ids: collections.abc.Iterable[int],
) -> sql.sql.StatementLambdaElement:
    """Delete statistics_short_term rows."""
    return sql.lambda_stmt(
        lambda: sql.delete(model.Events)
        .where(model.Events.event_id.in_(event_ids))
        .execution_options(synchronize_session=False)
    )


def delete_recorder_runs_rows(
    purge_before: dt.datetime, current_run_id: int
) -> sql.sql.StatementLambdaElement:
    """Delete recorder_runs rows."""
    return sql.lambda_stmt(
        lambda: sql.delete(model.RecorderRuns)
        .filter(model.RecorderRuns.start < purge_before)
        .filter(model.RecorderRuns.run_id != current_run_id)
        .execution_options(synchronize_session=False)
    )


def find_events_to_purge(purge_before: dt.datetime) -> sql.sql.StatementLambdaElement:
    """Find events to purge."""
    return sql.lambda_stmt(
        lambda: sql.select(model.Events.event_id, model.Events.data_id)
        .filter(model.Events.time_fired < purge_before)
        .limit(Const.MAX_ROWS_TO_PURGE)
    )


def find_states_to_purge(purge_before: dt.datetime) -> sql.sql.StatementLambdaElement:
    """Find states to purge."""
    return sql.lambda_stmt(
        lambda: sql.select(model.States.state_id, model.States.attributes_id)
        .filter(model.States.last_updated < purge_before)
        .limit(Const.MAX_ROWS_TO_PURGE)
    )


def find_short_term_statistics_to_purge(
    purge_before: dt.datetime,
) -> sql.sql.StatementLambdaElement:
    """Find short term statistics to purge."""
    return sql.lambda_stmt(
        lambda: sql.select(model.StatisticsShortTerm.id)
        .filter(model.StatisticsShortTerm.start < purge_before)
        .limit(Const.MAX_ROWS_TO_PURGE)
    )


def find_statistics_runs_to_purge(
    purge_before: dt.datetime,
) -> sql.sql.StatementLambdaElement:
    """Find statistics_runs to purge."""
    return sql.lambda_stmt(
        lambda: sql.select(model.StatisticsRuns.run_id)
        .filter(model.StatisticsRuns.start < purge_before)
        .limit(Const.MAX_ROWS_TO_PURGE)
    )


def find_latest_statistics_runs_run_id() -> sql.sql.StatementLambdaElement:
    """Find the latest statistics_runs run_id."""
    return sql.lambda_stmt(
        lambda: sql.select(sql.func.max(model.StatisticsRuns.run_id))
    )


def find_legacy_event_state_and_attributes_and_data_ids_to_purge(
    purge_before: dt.datetime,
) -> sql.sql.StatementLambdaElement:
    """Find the latest row in the legacy format to purge."""
    return sql.lambda_stmt(
        lambda: sql.select(
            model.Events.event_id,
            model.Events.data_id,
            model.States.state_id,
            model.States.attributes_id,
        )
        .outerjoin(model.States, model.Events.event_id == model.States.event_id)
        .filter(model.Events.time_fired < purge_before)
        .limit(Const.MAX_ROWS_TO_PURGE)
    )


def find_legacy_row() -> sql.sql.StatementLambdaElement:
    """Check if there are still states in the table with an event_id."""
    return sql.lambda_stmt(lambda: sql.select(sql.func.max(model.States.event_id)))
