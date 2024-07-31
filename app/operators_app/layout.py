"""Layout for the operators page.

editable_columns: a dictionary of {columns: bool} whether the columns should be editable by users.
empty_table_data: empty table data for default.
get_operator_layout: function that returns the Dash app layout for the operators page.
"""

from typing import List

import dash_ag_grid as dag
import pandas as pd
from dash import dcc
from dash import html

from app.connections import get_operator_data

# columns that can be edited by the user
editable_columns = {'id': False, 'first_name': True, 'last_name': True,
                    'initials': False, 'lam_1_certified': True,
                    'lam_2_certified': True, 'date_added': False,
                    'date_removed': False}

empty_table_data = [{k: None if 'certified' not in k else False for k in
                     editable_columns.keys()}]  # empty data if there isn't any to display


def get_operator_layout():
    """Get the Dash layout for the operators page."""

    response_dicts: List[dict] = get_operator_data()
    operators_data: pd.DataFrame = pd.DataFrame.from_records(response_dicts)

    column_defs = [{'field': k, 'editable': e} for k, e in editable_columns.items()]
    op_records = operators_data.to_dict('records')

    # layout styles
    operator_layout_div_style = {'display': 'block', 'height': '100%'}  # page parent div
    current_operators_div_style = {'height': '700px', 'width': '100%', 'display': 'inherit'}
    new_operator_div_style = {'height': '100px', 'width': '100%', 'position': 'initial'}
    operators_button_div_style = {'height': '5%', 'width': '100%', 'padding-left': '25%', 'padding-right': '25%'}

    # display the existing operators
    current_operators_div = html.Div(id='current_operators_div',
                                     style=current_operators_div_style,
                                     children=[dag.AgGrid(id='operator_ag_grid', columnDefs=column_defs,
                                                          rowData=op_records, style={'height': '100%'})])

    # an empty row on another grid to enter new operator data
    new_operator_div = html.Div(id='new_operator_div',
                                style=new_operator_div_style,
                                children=[dag.AgGrid(id='new_operator_ag_grid',
                                                     columnDefs=column_defs,
                                                     rowData=empty_table_data,
                                                     style={'height': '100%'})])

    # buttons for sending new or updated data to the server
    operators_button_div = html.Div(id='operators_button_div',
                                    style=operators_button_div_style,
                                    children=[
                                        html.Button('New operator', id='save_new_operator', n_clicks=0),
                                        html.Button('Save data', id='save_test_data', n_clicks=0),
                                        dcc.Store(id='test_data_store'),
                                        dcc.Store(id='new_op_data_store'),  # todo: do we need to store this here?
                                    ])

    # the page layout
    operator_layout = html.Div(id='operator_layout_div',
                               style=operator_layout_div_style,
                               children=[
                                   current_operators_div,
                                   new_operator_div,
                                   operators_button_div,
                               ])
    return operator_layout
