import os

import pandas as pd

from pv_self_cons.schemas import Consumer
from pv_self_cons.helpers import get_index


def get_consumption(consumer: Consumer) -> pd.Series:
    """Create a consumption profile for a consumer based on the VDEW data."""
    index = get_index()

    # create consumption profile from VDEW data
    path_consumption_profile_xls: str | None = os.getenv("path_consumption_profile_xls")
    assert path_consumption_profile_xls is not None, "Environment variable 'path_consumption_profile_xls' is not set."
    consumption: pd.Series = _create_consumption_profile(path_consumption_profile_xls, index, consumer.profile)

    # scale to yearly value
    cons = consumption / consumption.sum() * consumer.annual_consumption

    return cons


def _create_consumption_profile(path_consumption_profile_xls: str, index: pd.DatetimeIndex, profile: str) -> pd.Series:
    """Create a consumption profile for a consumer based on the VDEW data."""
    # read consumption profiles from excel
    consumption_raw = pd.read_excel(
        path_consumption_profile_xls,
        sheet_name=profile,
        header=[1, 2],
        index_col=0
    )[:-1].sort_index()

    index_local_time = index.tz_convert('Europe/Berlin')

    season = ['Winter' if m in [12, 1, 2] else 'Sommer' if m in [6, 7, 8] else 'Übergangszeit' for m in index.month]
    day_type = ['Samstag' if d == 5 else 'Sonntag' if d == 6 else 'Werktag' for d in index.dayofweek]

    consumption = pd.Series(
        index=index,
        data=[consumption_raw.loc[time, (s, d)] for time, s, d in zip(index_local_time.time, season, day_type)]
    )

    return consumption
