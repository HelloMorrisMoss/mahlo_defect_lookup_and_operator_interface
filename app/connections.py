from datetime import datetime
from traceback import format_exc

import pandas as pd
import requests

from untracked_config import defects_list_address


def get_defects(start_date: datetime = None, end_date=None):
    print(f'{start_date=}, {end_date=}')
    try:
        data = {
            'start_date': start_date.isoformat() if not isinstance(start_date, str) else start_date,
            'end_date': end_date.isoformat() if not isinstance(end_date, str) else end_date,
            }
        response = requests.get(defects_list_address, params=data)
        response_dict = response.json()
        defects_df = pd.DataFrame.from_dict(response_dict).T
        ts_columns = 'defect_start_ts', 'defect_end_ts', 'entry_created_ts', 'entry_modified_ts'
        for col in ts_columns:
            defects_df[col] = pd.to_datetime(defects_df[col]).dt.strftime('%Y-%m-%d %H:%M')
        return defects_df
    except Exception:
        print(f'Error fetching defect data: {format_exc()}')
