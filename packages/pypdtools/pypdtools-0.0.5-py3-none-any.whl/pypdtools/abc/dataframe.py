from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Awaitable, Iterator, Sized


class AbstractPtDataFrame(ABC, AsyncIterator, Awaitable, Sized, Iterator):
    """Abstract base class for DataFrame objects."""

    @abstractmethod
    def __repr__(self):
        ...

    @abstractmethod
    def __str__(self):
        ...

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...
