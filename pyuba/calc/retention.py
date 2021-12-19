from typing import Tuple

import numpy as np
import pandas as pd

from .acquisition import acquisition_events_cohort


def cohort_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.
    :param df: (pd.DataFrame)
    :return: (pd.DataFrame)

    Example
    -------
    Say you want to get the 3rd month for every user:
        df.sort(['UserId', 'OrderTime', inplace=True)
        df = df.groupby('UserId').apply(cohort_period)
        df[df.CohortPeriod == 3]
    """
    df["cohort_period"] = np.arange(len(df))
    return df


def load_cohorts(events: pd.DataFrame) -> pd.DataFrame:
    """
    make cohorts datasets
    :param events: (int)
                    make index random information
    :return: (DataFrame)
    """
    events = acquisition_events_cohort(events=events, acquisition_event_name="Install")
    events = events[events["user_active"]]
    grouped = events.groupby(["cohort", "event_period"])
    cohorts = grouped.agg({"distinct_id": pd.Series.nunique})
    return cohorts


def load_user_retention(cohorts: pd.DataFrame) -> pd.DataFrame:
    """
    make user retention datasets
    :param events: (int)
                    make index random information
    :return: (DataFrame)
    """
    cohorts = cohorts.astype(str).groupby(level=0).apply(cohort_period)
    cohorts = cohorts.astype(int)
    cohorts.reset_index(inplace=True)
    cohorts.set_index(["cohort", "cohort_period"], inplace=True)
    cohorts_size = cohorts["distinct_id"].groupby(level=0).first()
    cohorts_size = cohorts_size.astype(int)
    user_retention = cohorts["distinct_id"].unstack(0).divide(cohorts_size)
    return user_retention


def mask_retention_table(dim: Tuple[int]) -> np.ndarray:
    """
    Function used to fill NaN values with 0 above the diagonal line of the retention table and force
    the rest to be NaN.
    :param dim: (tuple)
                shape of retention dataframe (rows,columns)
    :return: (np.array)
                array used to mask which elements of the retention table can have values
    """
    # create an array of the same shape as the df and assign all elements =True
    mask = np.full(dim, True)

    # assign False where period for each row would no exist
    # i.e. if we have 10 weeks, the 1st week would have data for the next 9 weeks but the 2nd week would
    # only have data for the next 8 weeks, etc...
    for row in range(mask.shape[0]):
        mask[row, : mask.shape[0] - row] = False

    return mask


def split_revenue(
    sign_up: pd.DataFrame,
    payment: pd.DataFrame,
    resiual_rate_color: str = "lightgreen",
    payment_rate_color: str = "#ee1f5f",
    arppu_color="lightblue",
) -> pd.DataFrame:
    """
    Show Revenue Table
    :param sign_up: (pd.DataFrame)
                sign_up dataset
    :param payment: (pd.DataFrame)
                payment dataset
    :param resiual_rate_color: (str)
                resiual_rate feature bar color
    :param payment_rate_color: (str)
                payment_rate feature bar color
    :param arppu_color: (str)
                ARPPU feature bar color
    :return: (pd.DataFrame)
            revenue dataframe
    """
    try:
        sign_up["sign_up_month"] = sign_up["sign_up"].dt.month
        sign_up["last_login_month"] = sign_up["last_login"].dt.month

    except AttributeError:
        sign_up["sign_up"] = pd.to_datetime(sign_up["sign_up"])
        sign_up["last_login"] = pd.to_datetime(sign_up["last_login"])
        sign_up["sign_up_month"] = sign_up["sign_up"].dt.month
        sign_up["last_login_month"] = sign_up["last_login"].dt.month

    sign_up_dict = sign_up.groupby("user_id")["sign_up"].first().to_dict()
    payment["sign_up_month"] = payment["user_id"].map(sign_up_dict)
    payment["sign_up_month"] = payment["sign_up_month"].dt.month

    retention = (
        payment.groupby("user_id")
        .agg(
            payment_count=("payment", "count"),
            sales=("payment", "sum"),
            sign_up_month=("sign_up_month", "first"),
        )
        .reset_index()
    )

    retention = (
        retention.groupby("sign_up_month")
        .agg(buyer=("sign_up_month", "count"), sales=("sales", "sum"))
        .reset_index()
    )

    retention["sign_up_number"] = (
        sign_up.groupby("sign_up_month")["user_id"].count().values
    )
    retention["activate"] = (
        sign_up.groupby(["sign_up_month", "last_login_month"])["user_id"]
        .count()
        .unstack()
        .iloc[:, -1]
        .values
    )

    retention["residual_rate"] = (
        retention["activate"] / retention["sign_up_number"]
    ) * 100
    retention["payment_rate"] = (retention["buyer"] / retention["activate"]) * 100
    retention["ARPPU"] = retention["sales"] / retention["buyer"]

    retention = (
        retention.style.format(
            {
                "residual_rate": "{:.0f}%",
                "payment_rate": "{:.0f}%",
                "ARPPU": "{:.0f}",
            }
        )
        .bar(align="mid", subset=["residual_rate"], color=resiual_rate_color)
        .bar(align="mid", subset=["payment_rate"], color=payment_rate_color)
        .bar(align="mid", subset=["ARPPU"], color=arppu_color)
    )

    return retention
