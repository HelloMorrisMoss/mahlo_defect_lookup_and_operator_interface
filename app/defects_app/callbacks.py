import logging

from dash.dependencies import Input
from dash.dependencies import Output

from app.connections import get_defects

logger = logging.getLogger(__name__)


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
        defects_data = get_defects(start_date, end_date)

        # column_names = defects_data.columns
        columns = [
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in defects_data.columns
            ]
        new_data = defects_data.to_dict('records')
        return new_data, columns

    @dashapp.callback(
        Output("defect_table", "style_data_conditional"),
        [Input("defect_table", "active_cell")]
        )
    def update_selected_row_color(active):
        from app.defects_app.widgets.data_table import style_data
        style = style_data.copy()
        if active:
            style.append(
                {
                    "if": {"row_index": active["row"]},
                    "backgroundColor": "rgba(150, 180, 225, 0.2)",
                    "border": "1px solid blue",
                    },
                )
        return style

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
