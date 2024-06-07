import pandas as pd
from pv_self_cons.schemas import Consumer


def get_consumption(consumer: Consumer) -> pd.Series:
    return pd.Series([0.1] * 8760)
