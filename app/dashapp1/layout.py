# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html

from app.dashapp1.widgets import data_table
from app.dashapp1.widgets.datepicker import date_picker


table = data_table.datatable

layout = html.Div(id='main', children=[
    # dcc.Dropdown(
    #     id='my-dropdown',
    #     options=[{'label': a, 'value': b} for a, b in (('one', '1'), ('two', '2'))],
    #     value='1'
    #     ),
    date_picker,
    table,
    # dcc.Store(id='user-store'),
    ], style={'width': '500'})
