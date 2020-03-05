import calendar
import numpy as np
import uuid
import pickle
from pymemcache.client.base import Client
from pymemcache import serde


def serializer(key, value):
    return pickle.dumps(value), 1


def deserializer(key, value, flags):
    return pickle.loads(value)


PORT = 5555

# client = Client(('127.0.0.1', PORT), serializer=serializer, deserializer=deserializer)

client = Client(('localhost', PORT),
                serializer=serde.python_memcache_serializer,
                deserializer=serde.python_memcache_deserializer, timeout=120000)



MO, TU, WE, TH, FR, SA, SU = weekdays = range(7)

TARGET_COUNT = 10000
DAY_COUNT = 365
MAX_TIMES_PER_DAY = 2 * 3


def weekday_name(wd):
    return calendar.day_name[wd]


INTERESTING_TIMES_OF_DAY = [
    0,
    900,
    1200,
    1730,
    2145,
    2400
]

def get_ids_to_index(ids):
    return dict((_id, i) for i, _id in enumerate(ids))


def testing():
    a = np.empty((DAY_COUNT, TARGET_COUNT, MAX_TIMES_PER_DAY), np.dtype(np.int16))
    a.fill(-1)
    print(int(a.nbytes / 1024 / 1024), 'megabytes')

    # id_to_index = get_ids_to_index(random_ids)

    for day_index in range(0, DAY_COUNT):
        for target_index in range(TARGET_COUNT):
            for slot_index in range(4):
                a[day_index][target_index][slot_index] = (
                    INTERESTING_TIMES_OF_DAY[slot_index])
                
    #print(len(list(random_ids)))
    #print(random_ids[0:20])
    return a

def testing_save_memcached(a, client):
    client.set('days', pickle.dumps(a))
    return True

def testing_load_memcached():
    pickle.loads(client.get('days'))
    return True



