from typing import List, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure


def draw_user_retention(
    df: pd.DataFrame, width: int = 1550, height: int = 1550
) -> go.Figure:
    """
    draw user retention heatmap
    :params
        df: user retention dataframe
    :return
        (go.Figure)
    """
    z = df.values
    x = df.columns
    y = df.index
    annotations = []

    for n, row in enumerate(z):
        for m, val in enumerate(row):
            annotations.append(
                dict(
                    text="{0:.0%}".format(z[n][m]) if not np.isnan(z[n][m]) else "",
                    x=x[m],
                    y=y[n],
                    xref="x1",
                    yref="y1",
                    showarrow=False,
                )
            )

    layout = dict(
        title="Cohorts: User Retention",
        title_x=0.5,
        annotations=annotations,
        yaxis=dict(
            showgrid=False,
            tickmode="array",
            ticktext=y,
            autorange="reversed",
        ),
        xaxis=dict(showgrid=False),
        width=width,
        height=height,
        autosize=True,
    )
    trace = go.Heatmap(x=x, y=y, z=z, colorscale="Peach")
    fig = go.Figure(data=trace, layout=layout)
    fig.update_layout(uniformtext_minsize=6, uniformtext_mode="hide")

    return fig


def mau_plot(activate: Union[pd.Series, np.ndarray, List[float]]) -> Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            y=activate,
            mode="lines+markers",
            name="lines+markers",
        )
    )
    fig.update_xaxes(tickangle=30)

    return fig
