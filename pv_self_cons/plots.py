import pandas as pd
import plotly.graph_objects as go


def plot_self_consumption(
        pv_prod: pd.Series,
        consumption: pd.Series,
    ) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(x=pv_prod.index, y=pv_prod, name='PV production')
    fig.add_scatter(x=consumption.index, y=consumption, name='Consumption')
    self_consumption = pd.concat([pv_prod, consumption], axis=1).min(axis=1)
    fig.add_scatter(x=self_consumption.index, y=self_consumption, name='Self-consumption',
                    fill='tozeroy', fillcolor='rgba(144, 238, 144, 0.5)', mode='none')
    
    fig.update_layout(
        title="PV production and (self-)consumption",
        yaxis_title="[kWh / time slot]"
    )
    return fig
