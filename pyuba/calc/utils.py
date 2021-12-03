import math
from typing import Any, Dict, Optional

import pandas as pd
import plotly.graph_objects as go


def to_excel(
    df: pd.DataFrame, file_name: Optional[str] = None, sheet_name: Optional[str] = None
):
    """
    save excel files
    :df: (DataFrame)
                    events dataframe
    :file_name: (str)
                    named file name
    :sheet_name: (str)
                    named sheet name
    """
    if not file_name:
        file_name = "pyuba_output.xlsx"
    if not sheet_name:
        sheet_name = "sheet1"

    if not file_name.endswith(".xlsx"):
        file_name = file_name + ".xlsx"

    df.to_excel(file_name, sheet_name=sheet_name)


def to_json(df: pd.DataFrame, file_name: Optional[str] = None):
    """
    save json files
    :df: (DataFrame)
                    events dataframe
    :file_name: (str)
                    named file name
    :sheet_name: (str)
                    named sheet name
    """
    if not file_name:
        file_name = "pyuba_output.json"

    if not file_name.endswith(".json"):
        file_name = file_name + ".json"

    df.to_json(path_or_buf=file_name, orient="index")


def create_plotly_table(data: Dict[str, Optional[Any]]):
    """
    create plotly table
    :df: (DataFrame)
                    table dataset
    :return (go.Figure)
    """
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(data.keys()),
                    line_color="white",
                    fill_color="white",
                    font=dict(size=12, color="black"),
                    align="left",
                ),
                cells=dict(
                    values=[data.get(k) for k in data.keys()],
                    align="left",
                    fill=dict(color=[["#F9F9F9", "#FFFFFF"] * 5]),
                ),
            )
        ]
    )

    fig.update_layout(
        autosize=False,
        height=150,
        margin=dict(
            l=20,
            r=20,
            b=10,
            t=30,
        ),
    )

    return fig


def round_decimals_down(number: float, decimals: int = 2) -> float:
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def percentage_format(x: float) -> str:
    return f"{x:.0%}"
