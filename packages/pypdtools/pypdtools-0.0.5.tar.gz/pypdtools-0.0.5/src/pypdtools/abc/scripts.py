from abc import abstractmethod

from pypdtools.core.dataframe import PtDataFrame


class AbstractEtl(PtDataFrame):
    """This class is used to create an ETL object.

    Args:
        PtDataFrame (_type_): _description_
    """

    @abstractmethod
    def extract(self):
        """This method is used to get data from the source."""
        ...

    @abstractmethod
    def transform(self):
        """This method is used to transform the data."""
        ...

    @abstractmethod
    def load(self):
        """This method is used to load the data."""
        ...

    @abstractmethod
    def execute(self):
        """This method is used to execute the etl."""
        ...
