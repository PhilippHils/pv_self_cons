import pandas as pd
from pv_self_cons.schemas import PvSystem


def get_pv_prod(consumer: PvSystem) -> pd.Series:
    return pd.Series([0.2] * 8760)
