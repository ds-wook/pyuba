from typing import Optional

import pandas as pd


def to_excel(
    df: pd.DataFrame, file_name: Optional[str] = None, sheet_name: Optional[str] = None
):
    if not file_name:
        file_name = "pyuba_output.xlsx"
    if not sheet_name:
        sheet_name = "sheet1"

    if not file_name.endswith(".xlsx"):
        file_name = file_name + ".xlsx"

    df.to_excel(file_name, sheet_name=sheet_name)

    return None


def to_json(df: pd.DataFrame, file_name: Optional[str] = None):
    if not file_name:
        file_name = "pyuba_output.json"

    if not file_name.endswith(".json"):
        file_name = file_name + ".json"

    df.to_json(path_or_buf=file_name, orient="index")

    return None
