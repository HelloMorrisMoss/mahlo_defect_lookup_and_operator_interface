from datetime import datetime as dt

from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from flask_login import current_user
import pandas_datareader as pdr

from app.connections import get_defects

import logging

lg = logging.getLogger()


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('defect_table', 'defect_data'),
        Input('defect_start_ts_range_picker', 'start_date'),
        Input('defect_start_ts_range_picker', 'end_date'),
        # State('user-store', 'data')
        )
    def update_table(start_date, end_date):
        # '2022-02-27'
        # '2022-03-02T14:35:17.190967'

        return get_defects().to_dict('records')

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
