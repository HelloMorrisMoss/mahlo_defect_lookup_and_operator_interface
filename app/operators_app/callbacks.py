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
    @app.callback(Output('test_data_store', 'data'),
                  [Input('save_test_data', 'n_clicks'),
                   State('operator_ag_grid', 'rowData'),
                   # State('show_deactivated_operators_checkbox', 'value'),  # don't need, returns current data
                   ],
                  prevent_initial_call=True)
    def save_test_data(n_clicks, data):
        if n_clicks:
            # save changes made when the save button clicked
            updated_operator_df = pd.DataFrame.from_records(data)
            existing_operator_data = get_operator_data()
            eod_df = pd.DataFrame.from_records(existing_operator_data)
            new_rows_df = (pd.merge(updated_operator_df, eod_df, indicator=True, how='outer')
                           .query('_merge=="left_only"')
                           .drop('_merge', axis=1))


            # todo: can loop over the rows like this... or do it properly and send a list
            # this has finally overcome the 'not application/json' 415 error
            for (ri, row) in new_rows_df.iterrows():
                new_op_response = requests.put(operator_data_address, json=row.to_dict())

            # todo: probably request fresh data to return here...
            #  can maybe get away with if the response is affirmative then return the data as it was
            #  after it was changed. it SHOULD be fine, but leaves more opportunity for things that go
            #  wrong to be missed or propagate into further issues
            #  if done, add show_deactivated_operators_checkbox state to inputs to filter return data
        else:
            lg.debug(f'save_test_data ran without n_clicks: {n_clicks=}')
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
# TODO: logger, docstrings, handle connection failures

# app.clientside_callback(
#     """
#     function(params) {
#         var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};
#
#         dagfuncs.addEdits = function(params) {
#             console.log(params);  // Debugging line
#             if (!params.data) {
#                 console.log('addEdits was called with params.data undefined');
#             }
#             if (params && params.data && params.data.changes && params.colDef && params.colDef.field) {
#                 var newList = JSON.parse(params.data.changes);
#                 newList.push(params.colDef.field);
#                 params.data.changes = JSON.stringify(newList);
#             } else if (params && params.data && params.colDef && params.colDef.field) {
#                 params.data.changes = JSON.stringify([params.colDef.field]);
#             }
#             if (params && params.data && params.colDef && params.colDef.field) {
#                 params.data[params.colDef.field] = params.newValue;
#             }
#             console.log(params.data);  // Log the data after modification
#             return true;
#         };
#
#         dagfuncs.highlightEdits = function(params) {
#             console.log(params);  // Debugging line
#             if (!params.data) {
#                 console.log('highlightEdits was called with params.data undefined');
#             }
#             if (params && params.data && params.data.changes && params.colDef && params.colDef.field) {
#                 if (JSON.parse(params.data.changes).includes(params.colDef.field)) {
#                     return true;
#                 }
#             }
#             return false;
#         };
#
#         return dagfuncs;
#     }
#     """,
#     Output('operator_ag_grid', 'rowData', allow_duplicate=True),
#     Input('operator_ag_grid', 'cellValueChanged'),
#     prevent_initial_call=True,
# )


#     app.clientside_callback(
#         """
#         dagfuncs.highlightEdits = function(params) {
#     if (params.data) {
#     If (params.data.changes) {
#     if (JSON.parse(params.data.changes).includes(params.colDef.field))
#         {return true}
#     }
#     return false;
# }
# }
#         """,
#         Output('operator_ag_grid', 'rowData', allow_duplicate=True),
#         Input('operator_ag_grid', 'cellValueChanged'),
#         prevent_initial_call=True,
#     )


# app.clientside_callback(
#     """
#     function(data, scale) {
#     console.log(data);  // Debugging line
#     console.log(scale);  // Debugging line
#         return {
#             'data': data,
#             'layout': {
#                  'yaxis': {'type': scale}
#              }
#         }
#     }
#     """,
#     Output('clientside-graph', 'figure'),
#     Input('clientside-figure-store', 'data'),
#     Input('clientside-graph-scale', 'value')
# )
