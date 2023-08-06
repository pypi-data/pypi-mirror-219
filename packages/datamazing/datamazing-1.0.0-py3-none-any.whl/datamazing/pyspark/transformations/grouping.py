import pyspark.sql as ps
import pyspark.sql.functions as f

from datamazing._conform import _list


class Grouper:
    def __init__(self, df: ps.DataFrame, by: list[str]):
        self.df = df
        self.by = by

    def latest(self, on: str):
        version_window = ps.Window.partitionBy(self.by).orderBy(f.desc(on))
        return (
            self.df.withColumn("__version", f.row_number().over(version_window))
            .filter(f.col("__version") == 1)
            .drop("__version")
        )

    def pivot(self, on: list[str], values: list[tuple[str]] = None):
        """
        Pivot table. Non-existing combinations will be filled
        with NaNs.

        Args:
            on (list[str]): Columns which to pivot
            values (list[tuple[str]], optional): Enforce
                the existence of columns with these names
                after pivoting. Defaults to None, in which
                case the values will be inferred from the
                pivoting column.
        """
        if values:
            # if values is a list of tuples, concatenate these
            # so that they match the resulting pivoted columns
            values = [
                "_".join([str(item) for item in _list(value)]) for value in values
            ]

        remaining = set(self.df.columns).difference(_list(on), _list(self.by))

        df = (
            self.df.withColumn("__on", f.concat_ws("_", *_list(on)))
            .groupBy(self.by)
            .pivot("__on", values=values)
            .agg(*[f.first(col).alias(col) for col in remaining])
        )

        return df


def group(df: ps.DataFrame, by: list[str]):
    return Grouper(df, by)
