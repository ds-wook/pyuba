from typing import Tuple

import numpy as np
import pandas as pd

from .acquisition import acquisition_events_cohort


def cohort_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.
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
    events = acquisition_events_cohort(events=events, acquisition_event_name="Install")
    events = events[events["user_active"]]
    grouped = events.groupby(["cohort", "event_period"])
    cohorts = grouped.agg({"distinct_id": pd.Series.nunique})
    return cohorts


def load_user_retention(cohorts: pd.DataFrame) -> pd.DataFrame:
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
