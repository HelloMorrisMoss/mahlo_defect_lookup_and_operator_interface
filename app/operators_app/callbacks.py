from pprint import pformat

import requests
from dash import Output, Input, State

from app.operators_app.layout import get_operator_data, operator_data_address, empty_table_data


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
