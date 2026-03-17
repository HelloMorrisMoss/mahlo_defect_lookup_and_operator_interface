"""Register callbacks with the Dash app for the operators page.

register_operator_callbacks: function that registers the callbacks for the operator page.
"""

import pandas as pd
import requests
from dash import Output, Input, State

from __init__ import lg
from app.connections import get_operator_data
from app.operators_app.layout import empty_table_data
from untracked_config.server_address import operator_data_address

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def register_operator_callbacks(app):
    @app.callback(Output('operator_edits_store', 'data'),
                  [Input('save_operator_edits', 'n_clicks'),
                   State('operator_ag_grid', 'rowData'),
                   ],
                  prevent_initial_call=True)
    def save_operator_edits(n_clicks, data):
        if n_clicks:
            # save changes made when the save button clicked
            updated_operator_df = pd.DataFrame.from_records(data)
            existing_operator_data = get_operator_data()
            eod_df = pd.DataFrame.from_records(existing_operator_data)
            new_rows_df = (pd.merge(updated_operator_df, eod_df, indicator=True, how='outer')
                           .query('_merge=="left_only"')
                           .drop('_merge', axis=1))

            for (ri, row) in new_rows_df.iterrows():
                requests.put(operator_data_address, json=row.to_dict())

        else:
            lg.debug(f'save_operator_edits ran without n_clicks: {n_clicks=}')
        return data if n_clicks else None

    @app.callback([Output('operator_ag_grid', 'rowData', allow_duplicate=True),
                   Output('new_op_data_store', 'data'),
                   Output('new_operator_ag_grid', 'rowData')],
                  [Input('save_new_operator', 'n_clicks'),
                   State('new_operator_ag_grid', 'rowData'),
                   State('show_deactivated_operators_checkbox', 'value'),
                   ],
                  prevent_initial_call=True
                  )
    def save_new_operator(n_clicks, data, show_deactivated):
        """Add a new operator as entered into the new operator table.

        Updating the operator table and clearing the new op table."""
        if n_clicks > 0:
            new_op_response = requests.post(operator_data_address, json=data[0])
            if new_op_response.status_code in [200, 201]:
                return get_operator_data(
                    show_deactivated_operators=show_deactivated), empty_table_data, empty_table_data
            else:
                return None, None, None

    @app.callback(
        [Output('operator_ag_grid', 'rowData', allow_duplicate=True),
         Output('operator_ag_grid', 'selectedRows')],
        [Input('op_disenable_button', 'n_clicks'),
         State('operator_ag_grid', 'selectedRows'),
         State('show_deactivated_operators_checkbox', 'value'),
         # State('operator_ag_grid', 'rowData')
         ],
        prevent_initial_call=True)
    def disable_or_enable_selected_operator(n_clicks, selected_rows, show_deactivated):
        if selected_rows is not None:
            reselect_rows = [row.get('id') for row in selected_rows]
            for row in selected_rows:
                if row.get('date_removed') is None:
                    data_dict = {'id': row['id'], 'enabled': False}
                    response = requests.put(operator_data_address, json=data_dict)
                else:
                    data_dict = {'id': row['id'], 'enabled': True}
                    response = requests.put(operator_data_address, json=data_dict)

            # the js function works, but then it (not rows) will be what is returned by selectedRows next callback
            # reselect_fn = {'function': f'{reselect_rows} includes params.data.id'}  # javascript function
            updated_op_data = get_operator_data(show_deactivated_operators=show_deactivated)
            return updated_op_data, {'ids': reselect_rows}
        else:
            return None, None

    @app.callback(
        Output('operator_ag_grid', 'rowData'),
        [Input('show_deactivated_operators_checkbox', 'value'),  # Update the grid if new data is saved as well
         State('operator_ag_grid', 'rowData'), ],
        prevent_initial_call=True
    )
    def show_hide_deactivated_operators(checkbox_value, row_data):
        """When the show_deactivated_operators_checkbox is clicked, update the aggrid (table) based on the new value."""

        return get_operator_data(show_deactivated_operators=checkbox_value)
