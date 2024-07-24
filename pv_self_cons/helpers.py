import os

import pandas as pd


def get_index() -> pd.DatetimeIndex:
    year_simulation: str | None = os.getenv("year_simulation")
    assert year_simulation is not None, "Environment variable 'year_simulation' is not set."
    index = pd.date_range(
        start=f"{year_simulation}-01-01",
        end=f"{year_simulation}-12-31T23:45",
        freq='15min',
        tz='UTC'
    )
    return index
