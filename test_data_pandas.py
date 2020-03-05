import numpy as np
import pandas as pd


def scratch():
    # structure: days are main columns, other indices: slots first, then applicable targets
    pd.DataFrame(
        np.random.rand(8, 3),
        index=[['slot0', 'slot0', 'slot0', 'slot0',
                'slot1', 'slot1',
                'slot2', 'slot2'],
               ['oodi', 'kallio', 'herttoniemi', 'roihuvuori',
                'oodi',  'kallio',
                'oodi', 'kallio']],
        columns=['day1', 'day2', 'day3'])


INTERESTING_TIMES_OF_DAY = [
    0,
    200,
    300,
    400,
    1200,
    1730,
    2145,
    2400
]


NUM_TARGETS_TOTAL = 20000
NUM_TARGETS = {
    8: 5,
    6: 10,
    4: 100
}
NUM_DAYS = 365 * 2


def get_target_day(df, target, day):
    return df.loc[pd.IndexSlice[:, target], day]


def get_target(df, target):
    return df.loc[pd.IndexSlice[:, target], :]


def get_day(df, day):
    return df[day]


def get_target_day_range(df, target, start, end):
    return df.loc[pd.IndexSlice[:, target], start:end]


def get(df, target=None, day=None, start=None, end=None):
    if target is not None:
        if day is not None:
            return get_target_day(df, target, day)
        if start is not None and end is not None:
            return get_target_day_range(df, target, start, end)
        return get_target(df, target)
    if day is not None:
        return get_day(df, day)


def generate_table(targets, by_num_slots):
    def slot_id(i):
        # return 'slot{}'.format(i)
        return i

    def day_id(i):
        # return 'day{}'.format(i)
        return i

    slot_indices = []
    target_indices = []
    columns = [day_id(i) for i in range(NUM_DAYS)]

    for num_slots, targets in sorted(
            by_num_slots.items(),
            key=lambda x: (x[0], x[1])):

        for num in range(0, num_slots):
            for _ in range(0, len(targets)):
                slot_indices.append(slot_id(num))
            target_indices.extend(targets)

    assert len(slot_indices) == len(target_indices)

    random_table = np.random.randint(-1, high=125, size=(
        len(slot_indices), len(columns)), dtype=np.int16)
    df = pd.DataFrame(random_table,
                      index=[slot_indices, target_indices],
                      columns=[day_id(i) for i in range(NUM_DAYS)])
    return df


def test_targets():
    result = dict()
    by_num_slots = dict()
    target_id = 0
    for num_slots, num_targets in NUM_TARGETS.items():
        for _ in range(num_targets):
            # tid = 'target{}'.format(target_id)
            tid = target_id
            result[tid] = num_slots
            by_num_slots.setdefault(num_slots, set()).add(tid)
            target_id += 1
    for _ in range(NUM_TARGETS_TOTAL - len(result)):
        # tid = 'target{}'.format(target_id)
        tid = target_id
        result[tid] = 2
        by_num_slots.setdefault(2, set()).add(tid)
        target_id += 1

    return result, by_num_slots

# pseudo-algorithm:
# ================
# 1. sort targets by max number of slots -- get number
# 2. iterate days, iterate sorted targets
# 3. insert values into array
#
# btw: array size = iterate slots, sum number of targets per slot, (multiply by days)
#
