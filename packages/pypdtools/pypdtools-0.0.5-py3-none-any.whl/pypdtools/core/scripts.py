from typing import Iterator, List

import pandas as pd

from pypdtools.abc.scripts import AbstractEtl
from pypdtools.core.dataframe import PtDataFrame


class BaseEtl(AbstractEtl):
    """This class is used to create an ETL object."""

    def __init__(self) -> None:
        """This method is used to initialize the ETL object."""
        super().__init__()
        self._df = None
        self.executed = False

    def extract(self):
        """This method is used to get data from the source."""
        raise NotImplementedError

    def transform(self):
        """This method is used to transform the data."""
        raise NotImplementedError

    def load(self):
        """This method is used to load the data."""
        raise NotImplementedError

    def execute(self):
        """This method is used to execute the etl."""
        if self.executed:
            return self

        self.extract()
        self.transform()
        self.load()
        self.executed = True
        return self

    @property
    def data(self) -> pd.DataFrame:
        """This method is used to get the data."""
        self.execute()
        return self._df

    def __len__(self) -> int:
        """This method is used to get the length of the data."""
        self.execute()
        return super().__len__()

    def __iter__(self) -> Iterator:
        """This method is used to iterate over the data."""
        self.execute()
        return super().__iter__()

    def __aiter__(self) -> Iterator:
        """This method is used to async iterate over the data."""
        self.execute()
        return super().__aiter__()

    def __enter__(self) -> pd.DataFrame:
        """This method is used to enter the context."""
        self.execute()
        return super().__enter__()

    async def __aenter__(self) -> pd.DataFrame:
        """This method is used to async enter the context."""
        self.execute()
        return super().__aenter__()

    def __add__(self, other) -> PtDataFrame:
        """This method is used to add two dataframes."""
        self.execute()
        other.execute()
        return super().__add__(other)

    def __radd__(self, other) -> PtDataFrame:
        """This method is used to add two dataframes."""
        self.execute()
        other.execute()
        return super().__radd__(other)

    def col_to_list(self, col_name, drop_duplicates=True) -> List:
        """This method is used to get a column as a list."""
        self.execute()
        return super().col_to_list(col_name, drop_duplicates)
