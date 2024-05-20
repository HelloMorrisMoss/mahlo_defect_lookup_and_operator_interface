"""Register callbacks with the Dash app for the operators page.

register_operator_callbacks: function that registers the callbacks for the operator page.
"""

import requests
from dash import Output, Input, State

from app.connections import get_operator_data
from app.operators_app.layout import empty_table_data
from untracked_config import operator_data_address


def register_operator_callbacks(app):
    """Register callbacks with the Dash app for the operators page."""

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
