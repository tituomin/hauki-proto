# from dateutil.rrule import weekdays, rrule, rruleset, WEEKLY, MO
from datetime import timedelta

MO, TU, WE, TH, FR, SA, SU = WEEKDAYS = range(7)


class Slot:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    # def intersects(self, other):
    #     return (
    #         (self.start >= other.start and self.start <= other.end) or
    #         (self.end <= other.end and self.end >= other.start))

    # def assimilate(self, other):
    #     self.start = min(self.start, other.start)
    #     self.end = max(self.end, other.end)


# WEEKLY_RRULE = rrule(
#     WEEKLY,
#     # until=datetime(year=2020, month=12, day=31),
#     count=None,
#     interval=1,
#     wkst=MO)


class Period:  # TODO: this will be a django model
    def __init__(self, start, end, target):
        self.start = start
        self.end = end
        self.target = target
        self.slots = [None] * 7

    def get_priority(self):
        return self.end - self.start

    def set_slot(self, weekday, start, end):
        if weekday < 0 or weekday > 6:
            raise ValueError('Not a valid weekday: {}'.weekday)
        if self.slots[weekday] is None:
            self.slots[weekday] = []
        weekday_slots = self.slots[weekday]
        weekday_slots.append(Slot(start, end))

    def get_slots(self, weekday):
        weekday_slots = self.slots[weekday]
        return weekday_slots

    def get_slots_for_date(self, date):
        return self.get_slots(date.weekday())


class ConcreteDatePeriod:
    def __init__(self, start, length):
        self.start = start
        self.length = length
        self._internal_date_list = [{}] * self.length
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index > self.length:
            raise StopIteration
        result = self._get_date(self.index)
        self.index += 1
        return result

    def _get_date(self, index):
        return self.start + timedelta(index)

    def _get_weekday(self, index):
        return self._get_date(index).weekday

    def add_target(self, target, period):
        # TODO: check for period limits
        for i in range(self.length):
            weekday = self._get_weekday(i)
            target_slots = self._internal_date_list[i]
            target_slots[target] = period.get_slots(weekday)
