import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

a_day = datetime.timedelta(days=1)
a_month = relativedelta(months=1)

end_date = dt.today().date() + a_day
start_date = end_date - a_day * 2