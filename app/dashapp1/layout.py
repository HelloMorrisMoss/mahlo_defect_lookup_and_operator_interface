"""The layout for the dashboard app page."""

from dash import html

from app.dashapp1.default_dates import get_start_end_dates
from app.dashapp1.widgets import data_table
from app.dashapp1.widgets.datepicker import get_date_picker

start_date, end_date = get_start_end_dates()
table = data_table.datatable

layout = html.Div(id='main', children=[
    get_date_picker(start_date, end_date),
    table,
    # dcc.Store(id='user-store'),
    ], style={'width': '500'})
