from asyncio import Lock, sleep
from functools import reduce
from typing import Any, Awaitable, Iterator, List

import pandas as pd

from pypdtools.abc.dataframe import AbstractPtDataFrame


class PtDataFrame(AbstractPtDataFrame):
    """
    A class representing a Pandas DataFrame with additional functionality.

    Args:
        df (pd.DataFrame, optional): The Pandas DataFrame to be encapsulated. Defaults to an empty DataFrame.
    """

    def __init__(self, df: pd.DataFrame = pd.DataFrame()) -> None:
        """
        Initialize the PtDataFrame.

        Args:
            df (pd.DataFrame, optional): The Pandas DataFrame to be encapsulated. Defaults to an empty DataFrame.
        """
        self._df = df
        self._iterator = self._df.itertuples(index=False)
        self._lock = Lock()

    @property
    def df(self) -> pd.DataFrame:
        """
        Get the encapsulated Pandas DataFrame.

        Returns:
            pd.DataFrame: The encapsulated Pandas DataFrame.
        """
        return self._df

    def __repr__(self) -> str:
        """
        Return a string representation of the PtDataFrame.

        Returns:
            str: A string representation of the PtDataFrame.
        """
        return self._df.__repr__()

    def __str__(self) -> str:
        """
        Return a string representation of the PtDataFrame.

        Returns:
            str: A string representation of the PtDataFrame.
        """
        return self._df.__str__()

    def __await__(self) -> Awaitable:
        """
        Awaitable support for the PtDataFrame.

        Returns:
            Awaitable: An awaitable object.
        """
        return sleep(0.0001).__await__()

    def __enter__(self) -> pd.DataFrame:
        """
        Enter the context manager and return the encapsulated Pandas DataFrame.

        Returns:
            pd.DataFrame: The encapsulated Pandas DataFrame.
        """
        return self._df

    async def __aenter__(self) -> pd.DataFrame:
        """
        Asynchronous version of __enter__(). Enter the context manager and return the encapsulated Pandas DataFrame.

        Returns:
            pd.DataFrame: The encapsulated Pandas DataFrame.
        """
        return self._df

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context manager.

        Args:
            exc_type (type): The exception type, if any.
            exc_val (Exception): The exception instance, if any.
            exc_tb (traceback): The traceback, if any.
        """
        return None

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Asynchronous version of __exit__(). Exit the context manager.

        Args:
            exc_type (type): The exception type, if any.
            exc_val (Exception): The exception instance, if any.
            exc_tb (traceback): The traceback, if any.
        """
        return None

    def __aiter__(self) -> Iterator:
        """
        Asynchronous iterator support for the PtDataFrame.

        Returns:
            Iterator: An asynchronous iterator.
        """
        self._iterator = self._df.itertuples(index=False)

        async def _aiter() -> Iterator:
            """
            Asynchronous iterator helper function.

            Yields:
                Iterator: An item from the PtDataFrame.
            """
            while True:
                try:
                    yield self._iterator.__next__()
                except StopIteration:
                    break

        return _aiter()

    def __iter__(self) -> Iterator:
        """
               Iterator

        support for the PtDataFrame.

               Returns:
                   Iterator: An iterator.
        """
        self._iterator = self._df.itertuples(index=False)

        return (it for it in self._iterator)

    def __len__(self) -> int:
        """
        Return the length of the PtDataFrame.

        Returns:
            int: The length of the PtDataFrame.
        """
        return len(self._df)

    async def __anext__(self) -> Awaitable:
        """
        Asynchronous iterator support for the PtDataFrame.

        Returns:
            Awaitable: An awaitable object.
        """
        async with self._lock:
            try:
                return self._iterator.__next__()
            except StopIteration:
                raise StopAsyncIteration

    def __next__(self) -> Any:
        """
        Iterator support for the PtDataFrame.

        Returns:
            Any: An item from the PtDataFrame.
        """
        return self._iterator.__next__()

    def __add__(self, other) -> "PtDataFrame":
        """
        Concatenate the PtDataFrame with another PtDataFrame.

        Args:
            other (PtDataFrame): The PtDataFrame to concatenate.

        Returns:
            PtDataFrame: The concatenated PtDataFrame.
        """
        concat = pd.concat([self._df, other._df], ignore_index=True)
        return PtDataFrame(concat)

    def __iadd__(self, other) -> "PtDataFrame":
        """
        In-place concatenation of the PtDataFrame with another PtDataFrame.

        Args:
            other (PtDataFrame): The PtDataFrame to concatenate.

        Returns:
            PtDataFrame: The concatenated PtDataFrame.
        """
        self._df = pd.concat([self._df, other._df], ignore_index=True)
        return self

    @classmethod
    def reduce(cls, df_list) -> "PtDataFrame":
        """
        Reduce a list of PtDataFrame objects into a single PtDataFrame.

        Args:
            df_list (List[PtDataFrame]): The list of PtDataFrame objects to reduce.

        Returns:
            PtDataFrame: The reduced PtDataFrame.
        """
        return PtDataFrame(reduce(lambda x, y: x + y, df_list).df)

    def col_to_list(self, col_name, drop_duplicates=True) -> List:
        """
        Extract a column as a list from the PtDataFrame.

        Args:
            col_name (str): The name of the column to extract.
            drop_duplicates (bool, optional): Whether to drop duplicate values. Defaults to True.

        Returns:
            List: The column values as a list.
        """
        if drop_duplicates:
            return self._df[col_name].drop_duplicates().tolist()
        return self._df[col_name].tolist()
