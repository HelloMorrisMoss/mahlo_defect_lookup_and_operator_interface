import dash_bootstrap_components as dbc
import dash_core_components as dcc
# import dash_html_components as html
from dash import html
import dash_table

from app import data_table

data_table
table = data_table.datatable

# table_header = [
#     html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
#     ]
#
# row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
# row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
# row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
# row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])
#
# table_body = [html.Tbody([row1, row2, row3, row4])]
# table = dbc.Table(table_header + table_body,
#                   bordered=True,
#                   dark=True,
#                   hover=True,
#                   responsive=True,
#                   striped=True)

layout = html.Div(id='main', children=[
    html.H1(id='username'),
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': a, 'value': b} for a, b in (('one', '1'), ('two', '2'))],
        value='1'
        ),
    # dbc.Table(id='my-table'),
    table,
    dcc.Store(id='user-store'),
    ], style={'width': '500'})
