from datetime import timedelta


class CalendarRange:
    def __init__(self, start, end):
        self.length = (end - start).days
        self.start = start
        self._days = [None] * self.length

    def _get_index(self, date):
        index = (date - self.start).days
        if index < 0 or index >= self.length:
            raise ValueError(
                'Given date is not within range {}...{}(exclusive).'.format(
                    self.start.isoformat(),
                    (self.start+timedelta(days=self.length)).isoformat()))
        return index

    def get_date(self, date):
        return self._days[self._get_index(date)]

    def set_date(self, date, data):
        self._days[self._get_index(date)] = data

    def set_date_key(self, date, key, data):
        if self.get_date(date) is None:
            self.set_date(date, {})
        self.get_date(date)[key] = data

    def get_date_key(self, date, key):
        try:
            return self.get_date(date)[key]
        except TypeError:
            return None
        return None

    def __iter__(self):
        for i, el in enumerate(self._days):
            yield (self.start + timedelta(days=i), self._days[i])
