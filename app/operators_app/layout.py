# Libraries
import datetime

import dash
import pandas as pd
import requests
from dash import dcc
from dash import html, dash_table

# todo: move this to untracked_config
operator_data_address = 'http://10.155.0.21:5000/operator'


def get_operator_data():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=1)
    data = {
        'start_date': start_date.isoformat() if not isinstance(start_date, str) else start_date,
        'end_date': end_date.isoformat() if not isinstance(end_date, str) else end_date,
    }
    # response = requests.get(operator_data_address, params=data, timeout=20)
    response = requests.get(operator_data_address, timeout=20)
    return response.json()


editable_columns = {'id': False, 'first_name': True, 'last_name': True,
                    'initials': False, 'lam_1_certified': True,
                    'lam_2_certified': True, 'date_added': False,
                    'date_removed': False}
empty_table_data = [{k: None for k in editable_columns.keys()}]


def get_operator_layout():
    response_dict = get_operator_data()
    defects_dict = response_dict
    defects_df = pd.DataFrame.from_records(defects_dict)
    test_data = defects_df  # todo: just use response dict?
    saved_test_data = None

    # editable_columns

    # TODO: change this to a function - include the data from above
    operator_layout = html.Div(children=[dash_table.DataTable(columns=[{"name": i, "id": i} for i in test_data.columns],
                                                              data=test_data.to_dict('records'),
                                                              id='operator_data_table',
                                                              editable=True,
                                                              ),
                                         html.Button('Save data', id='save_test_data', n_clicks=0),
                                         dash_table.DataTable(
                                             columns=[{"name": i, "id": i, 'editable': editable_columns[i]} for i in
                                                      test_data.columns],
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


if __name__ == '__main__':
    # App
    app = dash.Dash(__name__)
    app.layout = get_operator_layout()
    app.run_server(debug=True, use_reloader=True)
