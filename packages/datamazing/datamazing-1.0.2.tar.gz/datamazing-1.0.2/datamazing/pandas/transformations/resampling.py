import pandas as pd


class Resampler:
    def __init__(self, df: pd.DataFrame, on: str, resolution: pd.Timedelta):
        self.df = df
        self.on = on
        self.resolution = resolution

    def agg(self, method: str):
        start_time = self.df[self.on].min()
        end_time = self.df[self.on].max()

        if method == "interpolate":
            aggregate_options = {"limit_area": "inside"}
        else:
            aggregate_options = {}

        df = (
            self.df.set_index(keys=self.on)
            .resample(rule=self.resolution)
            .aggregate(method, **aggregate_options)
            .reset_index()
        )

        if not df.empty:
            df = df[df[self.on].between(start_time, end_time)]

        return df


def resample(df: pd.DataFrame, on: str, resolution: pd.Timedelta):
    return Resampler(df, on, resolution)
