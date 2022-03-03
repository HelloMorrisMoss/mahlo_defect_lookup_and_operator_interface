from datetime import datetime as dt

from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from flask_login import current_user
import pandas_datareader as pdr

from app.connections import get_defects

import logging

from app.dashapp1.widgets.data_table import get_table_params

lg = logging.getLogger()


def register_callbacks(dashapp):
    pass
    @dashapp.callback(
        Output('defect_table', 'data'),
        Output('defect_table', 'columns'),
        Input('defect_start_ts_range_picker', 'start_date'),
        Input('defect_start_ts_range_picker', 'end_date'),
        # State('user-store', 'data')
        )
    def update_table(start_date, end_date):
        # '2022-02-27'
        # '2022-03-02T14:35:17.190967'
        print(f'dates! {start_date=}, {end_date=}')

        defects_data = get_defects(start_date, end_date)
        column_names = defects_data.columns
        columns = [
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in defects_data.columns
        ]
        new_data = defects_data.to_dict('records')
        print(f'new data {new_data}')
        return new_data, columns

    # @dashapp.callback(Input('defect_table', 'data'))
    # def data_table_updated(data):
    #     print('the data table data has been updated')

    # @dashapp.callback(
    #     Output('user-store', 'data'),
    #     Input('my-dropdown', 'value'),
    #     State('user-store', 'data'))
    # def cur_user(args, data):
    #     if current_user.is_authenticated:
    #         return current_user.username
    #
    # @dashapp.callback(Output('username', 'children'), Input('user-store', 'data'))
    # def username(data):
    #     if data is None:
    #         return ''
    #     else:
    #         return f'Hello {data}'
