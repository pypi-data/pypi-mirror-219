from abc import abstractmethod


class AbstractServiceLoader:
    """This class is used to create an AbstractServiceLoader object.

    Args:
        _type_ (_type_): _description_
    """

    @abstractmethod
    def load(self):
        """This method is used to load the service."""
        ...

    @abstractmethod
    def execute(self):
        """This method is used to execute the service."""
        ...
