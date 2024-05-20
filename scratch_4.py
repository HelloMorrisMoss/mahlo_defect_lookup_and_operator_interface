# Libraries
import datetime
from pprint import pformat

import dash
import pandas as pd
import requests
from dash import dcc
from dash import html, dash_table
from dash.dependencies import Input, Output, State

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


def register_operator_callbacks(app):
    # Callbacks
    @app.callback(Output('test_data_store', 'data'),
                  [Input('save_test_data', 'n_clicks'),
                   State('operator_data_table', 'data')])
    def save_test_data(n_clicks, data):
        # save changes made when the save button clicked
        print('save test data')
        return data if n_clicks else None

    @app.callback(Output('check_table', 'data'),
                  Input('test_data_store', 'data'))
    def restore_saved_test_data(data):
        # update the
        print('restore saved test data')
        # return data
        return get_operator_data()

    @app.callback(Output('output-container', 'value'),
                  Input('test_data_store', 'data'), )
    def display_stored_data(data):
        return pformat(data)

    @app.callback([Output('operator_data_table', 'data'),
                   Output('new_op_data_store', 'data'), ],
                  [Input('save_new_operator', 'n_clicks'),
                   State('new_operator_table', 'data')],
                  prevent_initial_call=True
                  )
    def save_new_operator(n_clicks, data):
        """Add a new operator as entered into the new operator table.

        Updating the operator table and clearing the new op table."""
        if n_clicks > 0:
            new_op_response = requests.post(operator_data_address, data=data[0])
            if new_op_response.status_code in [200, 201]:
                return get_operator_data(), empty_table_data
            else:
                print(new_op_response)
                return None, None


if __name__ == '__main__':
    # App
    app = dash.Dash(__name__)
    app.layout = get_operator_layout()
    app.run_server(debug=True, use_reloader=True)
