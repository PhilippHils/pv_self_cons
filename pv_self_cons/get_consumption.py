import os

import pandas as pd

from .schemas import Consumer


def get_consumption(consumer: Consumer) -> pd.Series:
    """Create a consumption profile for a consumer based on the VDEW data."""
    # create index
    year_simulation = os.getenv("year_simulation")
    index = pd.date_range(
        start=f"{year_simulation}-01-01",
        end=f"{year_simulation}-12-31T23:45",
        freq='15min',
        tz='Europe/Berlin'
    )

    # create consumption profile from VDEW data
    path_consumption_profile_xls = os.getenv("path_consumption_profile_xls")
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

    season = ['Winter' if m in [12, 1, 2] else 'Sommer' if m in [6, 7, 8] else 'Übergangszeit' for m in index.month]
    day_type = ['Samstag' if d == 5 else 'Sonntag' if d == 6 else 'Werktag' for d in index.dayofweek]

    consumption = pd.Series(
        index=index,
        data=[consumption_raw.loc[time, (s, d)] for time, s, d in zip(index.time, season, day_type)]
    )

    return consumption
