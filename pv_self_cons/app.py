import uvicorn
from fastapi import FastAPI
import pandas as pd
from pv_self_cons.get_comsumption import get_consumption
from pv_self_cons.get_pv_prod import get_pv_prod
from pv_self_cons.calculate_stats import calculate_stats
from pv_self_cons.schemas import RunRequestBody

app = FastAPI(
    root_path="/api/v0",
    title="pv_self_cons API",
    description="Estimate your PV self consumption",
    version="0.0.1",
    contact={
        'name': 'Philipp Hilsheimer',
        'email': 'philipp.hilsheimer@gmail.com'
    }
)


@app.get("/")
def read_root() -> dict:
    return {"Welcome": "to the API of the pv_self_cons package. "
            + "Please use the /docs endpoint to see the swagger documentation. "
            }


@app.get("/consumption_profiles")
def get_consumption_profiles() -> dict:
    return {"profiles": ["profile_1", "profile_2"]}


@app.post("/run")
def post_run(body: RunRequestBody) -> dict:

    pv_prod_total = pd.Series([0.0] * 8760)
    for pvsystem in body.pvsystems:
        pv_prod: pd.Series = get_pv_prod(pvsystem)
        pv_prod_total = pv_prod_total.add(pv_prod)

    consumption_total = pd.Series([0.0] * 8760)
    for consumer in body.consumers:
        consumption: pd.Series = get_consumption(consumer)
        consumption_total = consumption_total.add(consumption)

    stats: dict = calculate_stats(pv_prod_total, consumption_total)

    return stats


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
