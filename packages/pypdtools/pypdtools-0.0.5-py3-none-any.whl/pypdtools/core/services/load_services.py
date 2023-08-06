import math
from pathlib import Path

import pandas as pd

from pypdtools.abc.services import AbstractServiceLoader


class LoadToCsv(AbstractServiceLoader):
    """This class is used to create a LoadToCsv object.

    Args:
        df (pd.DataFrame): The DataFrame to load.
        path (str): The path to the CSV file.
    """

    def __init__(self, df: pd.DataFrame, path: str, quotechar='"', index=False, *args, **kwargs) -> None:
        """This method is used to initialize the LoadToCsv object."""
        self._df = df
        self._path = Path(path)
        self._quotechar = quotechar
        self._index = index
        self._args = args
        self._kwargs = kwargs

    def load(self) -> None:
        """This method is used to load the service."""
        self._df.to_csv(
            path_or_buf=self._path, quotechar=self._quotechar, index=self._index, *self._args, **self._kwargs
        )

    def execute(self) -> None:
        """This method is used to execute the service."""
        self.load()


class LoadToSql(AbstractServiceLoader):
    """This class is used to create a LoadToSql object.

    Args:
        df (pd.DataFrame): The DataFrame to load.
        con (sqlalchemy.engine.base.Connection): The SQLAlchemy connection object.
        table_name (str): The name of the table to load.
        schema (str, optional): The schema of the table to load. Defaults to None.
        if_exists (str, optional): The action to take if the table already exists. Defaults to "append".
        index (bool, optional): Whether or not to include the DataFrame index. Defaults to False.
    """

    def __init__(
        self, df: pd.DataFrame, con, table_name, schema=None, if_exists="append", index=False, *args, **kwargs
    ) -> None:
        """This method is used to initialize the LoadToSql object."""
        self._df = df
        self._con = con
        self._table_name = table_name
        self._schema = schema
        self._if_exists = if_exists
        self._index = index
        self._args = args
        self._kwargs = kwargs

    def load(self) -> None:
        """This method is used to load the service."""

        def chunksize_calc():
            """This method is used to calculate the chunksize."""
            chunksize = math.floor(2097 / len(self._df.columns))
            return 1000 if chunksize > 1000 else chunksize

        self._df.to_sql(
            name=self._table_name,
            con=self._con,
            schema=self._schema,
            if_exists=self._if_exists,
            index=self._index,
            chunksize=chunksize_calc(),
            *self._args,
            **self._kwargs,
        )

    def execute(self) -> None:
        """This method is used to execute the service."""
        self.load()
