# Standard Library
from abc import ABC, abstractmethod

# First Party
from engines import response


class engine(ABC):
    @abstractmethod
    async def get(self, url: str, **kwargs) -> response:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass
