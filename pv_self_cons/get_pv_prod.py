import os
from io import StringIO

import json
import requests
import pandas as pd

from pv_self_cons.schemas import PvSystem
from pv_self_cons.helpers import get_index


def get_pv_prod(pvsystem: PvSystem) -> pd.Series:
    year_simulation: str | None = os.getenv("year_simulation")
    assert year_simulation is not None, "Environment variable 'year_simulation' is not set."

    args = {
        'lat': pvsystem.latitude,
        'lon': pvsystem.longitude,
        'date_from': year_simulation + '-01-01',
        'date_to': str(int(year_simulation) + 1) + '-01-01',
        'dataset': 'merra2',
        'capacity': 1.0,                                                                              # capacity set to 1 to generate capacity factor units
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': pvsystem.tilt,
        'azim': pvsystem.azimuth,
        'format': 'json'
    }

    url = 'https://www.renewables.ninja/api/data/pv'
    token: str | None = os.getenv("renewables_ninja_token")
    assert token is not None, "Environment variable 'renewables_ninja_token' is not set."

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
    production.index = production.index.tz_localize(parsed_response['metadata']['units']['time']).tz_convert('UTC')
    index = get_index()

    return production.loc[index]
