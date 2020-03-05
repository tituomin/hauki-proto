import calendar
import time
# from hypothesis import given, settings, example
# import hypothesis.strategies as st

from pymemcache.client.base import Client
from pymemcache import serde

PORT = 32768
client = Client('localhost', PORT,
                serializer=serde.python_memcache_serializer,
                deserializer=serde.python_memcache_deserializer)

MO, TU, WE, TH, FR, SA, SU = weekdays = range(7)

TARGET_COUNT = 20000
DAY_COUNT = 365


def weekday_name(wd):
    return calendar.day_name[wd]


# @st.composite
# @example((24,0))
# def test_time_of_day(draw):
#     return draw(st.tuples(
#         st.integers(min_value=0, max_value=23),
#         st.integers(min_value=0, max_value=59)))
INTERESTING_TIMES_OF_DAY = [
    (0, 0),
    (9, 0),
    (12, 0),
    (17, 30),
    (21, 45),
    (24, 0)]


#@st.composite
#def test_day(draw):
def test_slot(index):
    #closed_dice = draw(st.integers(min_value=1, max_value=24))
    closed = (index % 48 == 0)
    if closed:
        return None
    else:
        return (INTERESTING_TIMES_OF_DAY[index % len(INTERESTING_TIMES_OF_DAY)],
                INTERESTING_TIMES_OF_DAY[(index + 1) % len(INTERESTING_TIMES_OF_DAY)])


#@st.composite
def test_day(day_index):
    #draw(st.lists(test_day(), min_size=100, max_size=DAY_COUNT))
    def test_target(index):
        return (('unit', index),
                {'hours': [test_slot(day_index + index)],
                 'period': 'periodX'})

    return dict(
        (test_target(target_index) for target_index in range(TARGET_COUNT)))


# @given(test_targets())
# @settings(max_examples=100000)
def testing_scratch():
    days = [None] * DAY_COUNT
    for i in range(0, (2 * DAY_COUNT), 2):
        days[int(i/2)] = test_day(i)
    print(len(days))
    return days


def testing_mutate(days):
    for i in range(0, (2 * DAY_COUNT), 2):
        days[i][('unit', 5)] = {'hours': [(1,2),(3,4),(5,6),(7,8)], 'period': 'periodY'}
    return days


def testing_pickle_to_memcached(days):
    client.set('days', days)



def testing_unpickle_from_memcached(days):
    return client.get(days)
