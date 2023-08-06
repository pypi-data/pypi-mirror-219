from functools import reduce

import pandas as pd


def latest(
    df: pd.DataFrame,
    on: str,
):
    s = df.sort_values(by=on).iloc[-1]
    s.name = None
    return s


def merge(
    dfs: list[pd.DataFrame],
    on: list[str],
    how: str = "inner",
) -> pd.DataFrame:
    return reduce(lambda df1, df2: df1.merge(df2, on=on, how=how), dfs)


def shift_time(
    df: pd.DataFrame,
    on: str,
    period: pd.Timedelta,
):
    df = df.copy()
    df[on] = df[on] + period
    return df


def unique_one(s: pd.Series) -> object:
    if len(s.unique()) > 1:
        raise ValueError("Series has more than one unique value")
    return s.iloc[0]
