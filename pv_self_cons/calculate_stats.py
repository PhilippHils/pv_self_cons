import numpy as np
import pandas as pd


def calculate_stats(pv_prod: pd.Series, consumption: pd.Series) -> dict[str, float]:
    assert (pv_prod.index == consumption.index).all(), \
        "Index of pv_prod and consumption must be equal"
    pv_prod_sum: float = pv_prod.sum()
    consumption_sum: float = consumption.sum()

    self_consumption = pd.concat([pv_prod, consumption], axis=1).min(axis=1)

    ratio_consumption_production: float = pv_prod_sum / consumption_sum
    fraction_of_consumption_covered: float = self_consumption.sum() / consumption_sum
    fraction_of_pv_prod_consumed: float = self_consumption.sum() / pv_prod_sum

    return {
        "Annual PV production [kWh]": pv_prod_sum,
        "Annual consumption [kWh]": consumption_sum,
        "Ratio of production over consumption": ratio_consumption_production,
        "Fraction of consumption covered": fraction_of_consumption_covered,
        "Fraction of PV production consumed": fraction_of_pv_prod_consumed
    }
