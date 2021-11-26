import random

import numpy as np
import pandas as pd


def load_dataset(index_range: int = 10000, id_range: int = 5000) -> pd.DataFrame:
    # instantiate a dataframe with 100,000 rows
    events = pd.DataFrame(
        {"distinct_id": 0, "name": None, "time": pd.NaT, "user_source": None},
        index=list(range(index_range)),
    )
    # define lists to choose randomly from to populate all the rows
    distinct_id_list = (
        np.arange(id_range) + 1
    )  # 5,000 distinct users with ids starting from 1
    name_list = [
        "Install",
        "SignUp",
        "Click Product",
        "Purchase",
        "Change Adress",
        "Cancel Order",
        "Accept Conditions",
    ]
    date_list = pd.date_range(start="2018-01-01", end="2019-01-01", freq="H")
    user_source_list = ["Organic", "Non-organic"]

    # generate distinct_id, name and time columns
    events["distinct_id"] = events["distinct_id"].apply(
        lambda x: random.choice(distinct_id_list)
    )
    events["name"] = events["name"].apply(lambda x: random.choice(name_list))
    events["time"] = events["time"].apply(lambda x: random.choice(date_list))

    # generate user_source column which is based on distinct_id column
    user_source_dict = {
        uid: random.choice(user_source_list) for uid in events["distinct_id"].unique()
    }
    events["user_source"] = events["distinct_id"].map(user_source_dict)

    return events
