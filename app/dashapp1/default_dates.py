import datetime
from datetime import datetime as dt

from dateutil.relativedelta import relativedelta

A_DAY = datetime.timedelta(days=1)
A_MONTH = relativedelta(months=1)


def get_start_end_dates():
    """Get the default start and end dates for today."""

    end_date = dt.today().date() + A_DAY
    start_date = end_date - A_DAY * 2
    return start_date, end_date
