"""Layout for the operators page.

editable_columns: a dictionary of {columns: bool} whether the columns should be editable by users.
empty_table_data: empty table data for default.
get_operator_layout: function that returns the Dash app layout for the operators page.
"""

from typing import List

import pandas as pd
from dash import dcc
from dash import html, dash_table

from app.connections import get_operator_data

# columns that can be edited by the user
editable_columns = {'id': False, 'first_name': True, 'last_name': True,
                    'initials': False, 'lam_1_certified': True,
                    'lam_2_certified': True, 'date_added': False,
                    'date_removed': False}
empty_table_data = [{k: None for k in editable_columns.keys()}]  # empty data if there isn't any to display


def get_operator_layout():
    """Get the Dash layout for the operators page."""

    response_dicts: List[dict] = get_operator_data()
    operators_data: pd.DataFrame = pd.DataFrame.from_records(response_dicts)
    saved_test_data = None

    operator_layout = html.Div(children=[
        # the table of operators
        dash_table.DataTable(columns=[{"name": i, "id": i} for i in operators_data.columns],
                             data=operators_data.to_dict('records'),
                             id='operator_data_table',
                             editable=True,
                             ),
        html.Button('Save data', id='save_test_data', n_clicks=0),
        dash_table.DataTable(
            columns=[{"name": key, "id": key, 'editable': editable_columns[key]} for
                     key in editable_columns.keys()],
            data=empty_table_data,
            id='new_operator_table',
        ),
        html.Button('New operator', id='save_new_operator', n_clicks=0),
        dcc.Store(id='test_data_store'),
        dcc.Store(id='new_op_data_store'),  # todo: do we need to store this here?
        dash_table.DataTable(id='check_table', data=saved_test_data),
        dcc.Textarea(id='output-container', value="text")
    ],
        style={'width': '50%', 'display': 'inline-block', 'padding-left': '25%',
               'padding-right': '25%'}
    )
    return operator_layout
