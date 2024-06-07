import pandas as pd


def calculate_stats(pv_prod: pd.Series, consumption: pd.Series) -> dict:
    pv_prod_sum: float = pv_prod.sum()
    consumption_sum: float = consumption.sum()

    fraction_of_consumption_covered_yearly: float = pv_prod_sum / consumption_sum
    fraction_of_consumption_covered_hourly: float = 0  # TODO
    fraction_of_pv_prod_consumed_hourly: float = 0  # TODO

    return {
        "Annual PV production [kWh]": pv_prod_sum,
        "Annual consumption [kWh]": consumption_sum,
        "Fraction of consumption covered yearly": fraction_of_consumption_covered_yearly,
        "Fraction of consumption covered, hour by hour": fraction_of_consumption_covered_hourly,
        "Fraction of PV production consumed, hour by hour": fraction_of_pv_prod_consumed_hourly
    }
