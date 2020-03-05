from datetime import datetime

from dateutil.relativedelta import relativedelta
from dateutil.easter import easter
from dateutil.rrule import rrule, rruleset, YEARLY, MO, TU, WE, TH, FR, SA, SU, WEEKLY
from dateutil.parser import parse


basic_opening_hour_set = rruleset()

weekly_rrule = rrule(
    WEEKLY,
    until=datetime(year=2020, month=12, day=31),
    count=None,
    interval=1,
    wkst=MO)


mon_open = weekly_rrule.replace(
    byweekday=MO,
    dtstart=datetime(year=2020,
                     month=1,
                     day=1,
                     hour=9,
                     minute=30))


mon_close = weekly_rrule.replace(
    byweekday=MO,
    dtstart=datetime(year=2020,
                     month=1,
                     day=1,
                     hour=17,
                     minute=30))


tue_open = weekly_rrule.replace(
    byweekday=TU,
    dtstart=datetime(year=2020,
                     month=1,
                     day=1,
                     hour=10,
                     minute=30))


tue_close = weekly_rrule.replace(
    byweekday=TU,
    dtstart=datetime(year=2020,
                     month=1,
                     day=1,
                     hour=16,
                     minute=30))


basic_opening_hour_set.rrule(mon_open)
basic_opening_hour_set.rrule(mon_close)
basic_opening_hour_set.rrule(tue_open)
basic_opening_hour_set.rrule(tue_close)


for d in basic_opening_hour_set:
    print(d.isoformat(), d.strftime('%a'))
