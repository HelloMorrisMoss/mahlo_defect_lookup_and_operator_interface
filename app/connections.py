from datetime import datetime
from traceback import format_exc
from typing import List

import pandas as pd
import requests

from __init__ import lg
from untracked_config.server_address import defects_list_address, operator_data_address


def get_defects(start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
    """Get the defect records within the date range from the database-service."""

    print(f'{start_date=}, {end_date=}')
    try:
        data = {
            'start_date': start_date.isoformat() if not isinstance(start_date, str) else start_date,
            'end_date': end_date.isoformat() if not isinstance(end_date, str) else end_date,
            }
        response = requests.get(defects_list_address, params=data, timeout=20)
        response_dict = response.json()
        defects_columns = response_dict['default_column_order']
        defects_dict = response_dict['results_dict']
        defects_df = pd.DataFrame.from_dict(defects_dict).T
        defects_df = defects_df[defects_columns]
        if not len(defects_df):
            print('No records found')
            defects_df = pd.DataFrame.from_dict({'defect_data': ['No Records Found.']})
        else:
            for idx, col in enumerate(defects_df):  # loop through all columns
                if col.endswith('_ts') or col.endswith('_time'):
                    defects_df[col] = pd.to_datetime(defects_df[col]).dt.tz_localize(None)  # excel can't do timezones
                    defects_df[col] = defects_df[col].dt.round(
                        '1s')  # don't need milliseconds here and columns wind up too wide with empty space
        return defects_df
    except Exception:
        print(f'Error fetching defect data: {format_exc()}')
        return pd.DataFrame.from_dict({'defect_data': ['failed to load']})


def get_operator_data(show_deactivated_operators=False) -> List[dict]:
    """Get the operators data from the Mahlo popup server as a list of dictionaries."""

    response = requests.get(operator_data_address, timeout=20)
    lg.debug(f'{operator_data_address=}')
    lg.debug(f'{response=}')
    lg.debug(f'{response.content=}')
    lg.debug(f'{response.text=}')

    if not show_deactivated_operators:
        return_json = [op for op in response.json() if op.get('date_removed') is None]
    else:
        return_json = response.json()
    return return_json
