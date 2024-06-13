import os
from io import StringIO

import json
import requests
import pandas as pd

from .schemas import PvSystem


def get_pv_prod(pvsystem: PvSystem) -> pd.Series:
    year_simulation = int(os.getenv("year_simulation"))

    args = {
        'lat': pvsystem.latitude,
        'lon': pvsystem.longitude,
        'date_from': str(year_simulation) + '-01-01',
        'date_to': str(year_simulation + 1) + '-01-01',
        'dataset': 'merra2',
        'capacity': 1.0,                                                                              # capacity set to 1 to generate capacity factor units
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': pvsystem.tilt,
        'azim': pvsystem.azimuth,
        'format': 'json'
    }

    url = 'https://www.renewables.ninja/api/data/pv'
    token: str = os.getenv("renewables_ninja_token")

    s = requests.session()
    s.headers = {'Authorization': 'Token ' + token}
    r = s.get(url, params=args)

    assert r.status_code == 200, f"Request failed with status code {r.status_code}"

    # Parse JSON to get a pandas.DataFrame of data and dict of metadata
    parsed_response = json.loads(r.text)

    production_raw: pd.Series = pd.read_json(
        StringIO(json.dumps(parsed_response['data'])),
        orient='index'
    ).squeeze()

    production = production_raw.resample('15min').interpolate() / 4
    production = production.loc[production.index.year == year_simulation]

    return production
