import pandas as pd
import requests
from datetime import datetime

from untracked_config import defects_list_address


def get_defects(start_date:datetime = None, end_date=None):
    print(f'{start_date=}, {end_date=}')
    data = {
        'start_date': start_date.isoformat() if not isinstance(start_date, str) else start_date,
        'end_date': end_date.isoformat() if not isinstance(end_date, str) else end_date,
            }
    response = requests.get(defects_list_address, params=data)
    return pd.DataFrame.from_dict(response.json()).T
