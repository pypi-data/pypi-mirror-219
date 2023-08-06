import asyncio
from typing import Awaitable, Iterator, List


class AsyncCollection:
    """A class that allows for asynchronous iteration over a collection.

    Args:
        collection (iterable): The collection to iterate over.

    Attributes:
        collection (iterable): The collection to iterate over.
    """

    def __init__(self, collection):
        self.collection = collection

    async def __aiter__(self) -> Iterator:
        """Asynchronously iterate over the collection.

        Yields:
            Any: The next item in the collection.
        """
        for item in self.collection:
            yield item
            await asyncio.sleep(0)

    async def __anext__(self) -> Awaitable:
        """Asynchronously get the next item in the collection.

        Raises:
            StopAsyncIteration: If there are no more items in the collection.

        Returns:
            Any: The next item in the collection.
        """
        try:
            item = next(self.iterator)
        except StopIteration:
            raise StopAsyncIteration
        else:
            await asyncio.sleep(0)
            return item

    async def __aenter__(self) -> "AsyncCollection":
        """Enter the async context.

        Returns:
            AsyncCollection: This object.
        """
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Exit the async context.

        Args:
            exc_type (type): The type of the exception (if any).
            exc (Exception): The exception instance (if any).
            tb (traceback): The traceback object (if any).
        """
        pass

    async def map(self, func) -> List:
        """Asynchronously apply a function to each item in the collection.

        Args:
            func (callable): The function to apply.

        Returns:
            List: A list of the results of applying the function to each item in the collection.
        """
        tasks = []
        for item in self.collection:
            tasks.append(asyncio.ensure_future(func(item)))
        results = await asyncio.gather(*tasks)
        return results
