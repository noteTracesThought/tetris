from cycle.cycle_types import CYCLE_ID

from cycle.cycle_process import (
    cycle_process_10ms,
    cycle_process_50ms,
    cycle_process_100ms,
    cycle_process_500ms,
    cycle_process_1000ms,
)

cycle_index = (
    (CYCLE_ID.ID_1,    1,     None),
    (CYCLE_ID.ID_2,    2,     None),
    (CYCLE_ID.ID_4,    4,     None),
    (CYCLE_ID.ID_10,   10,    cycle_process_10ms),
    (CYCLE_ID.ID_50,   50,    cycle_process_50ms),
    (CYCLE_ID.ID_100,  100,   cycle_process_100ms),
    (CYCLE_ID.ID_500,  500,   cycle_process_500ms),
    (CYCLE_ID.ID_1000, 1000,  cycle_process_1000ms),
)
