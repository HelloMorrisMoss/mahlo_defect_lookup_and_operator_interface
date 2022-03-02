import dash_bootstrap_components as dbc
import dash_core_components as dcc
# import dash_html_components as html
from dash import html
import dash_table

from app import data_table

table = data_table.datatable


layout = html.Div(id='main', children=[
    html.H1(id='username'),
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': a, 'value': b} for a, b in (('one', '1'), ('two', '2'))],
        value='1'
        ),
    table,
    dcc.Store(id='user-store'),
    ], style={'width': '500'})
