from datetime import datetime as dt
import datetime
from dash import dcc


today = dt.today()

date_picker = dcc.DatePickerRange(
    id='defect_start_ts_range_picker',  # ID to be used for callback
    calendar_orientation='horizontal',  # vertical or horizontal
    day_size=39,  # size of calendar image. Default is 39
    end_date_placeholder_text="Return",  # text that appears when no end date chosen
    with_portal=False,  # if True calendar will open in a full screen overlay portal
    first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
    reopen_calendar_on_clear=True,
    is_RTL=False,  # True or False for direction of calendar
    clearable=True,  # whether or not the user can clear the dropdown
    number_of_months_shown=1,  # number of months shown when calendar is open
    min_date_allowed=dt(2021, 11, 1),  # minimum date allowed on the DatePickerRange component
    max_date_allowed=today,  # maximum date allowed on the DatePickerRange component
    initial_visible_month=today,  # the month initially presented when the user opens the calendar
    start_date=today - datetime.timedelta(days=1),
    end_date=today,
    display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
    month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
    minimum_nights=2,  # minimum number of days between start and end date

    persistence=True,
    persisted_props=['start_date'],
    persistence_type='session',  # session, local, or memory. Default is 'local'

    updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
    )