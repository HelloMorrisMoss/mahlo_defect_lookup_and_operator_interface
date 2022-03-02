import pandas as pd
import requests

from untracked_config import defects_list_address


def get_defects(start_date=None, end_date=None):
    response = requests.get(defects_list_address)
    return pd.DataFrame.from_dict(response.json()).T