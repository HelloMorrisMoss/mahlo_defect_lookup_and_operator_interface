import pandas as pd
from dash import dash_table

from app.connections import get_defects
from app.dashapp1.default_dates import get_start_end_dates


def get_table_params(table_defects_data: pd.DataFrame):
    """Get the parameter dictionary for the data table using the data provided."""

    return dict(
        id='defect_table',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in table_defects_data.columns
            ],
        data=table_defects_data.to_dict('records'),  # the contents of the table
        editable=True,  # allow editing of data inside all cells
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",  # allow users to select 'multi' or 'single' rows
        row_deletable=True,  # choose if user can delete a row (True) or not (False)
        selected_columns=[],  # ids of columns that user selects
        selected_rows=[],  # indices of rows that user selects
        page_action="native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        page_size=25,  # number of rows visible per page
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'width': 95
            },

        # style_cell_conditional=[    # align text columns to left. By default they are aligned to right
        #     {
        #         'if': {'column_id': c},
        #         'textAlign': 'left'
        #     } for c in ['country', 'iso_alpha3']
        # ],
        style_data={  # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
            }
        )


def get_datatable(param_dict):
    """Get the datatable object using the provided parameter dictionary."""

    return dash_table.DataTable(**param_dict)


start_date, end_date = get_start_end_dates()
defects_data = get_defects(start_date, end_date)
if defects_data is not None:
    defect_table_params = get_table_params(defects_data)
    datatable = get_datatable(defect_table_params)
else:
    print('No defect data.')
