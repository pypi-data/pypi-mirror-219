from typing import Any, Union

from datetime import datetime

from abc import ABC, abstractmethod


class BaseAsyncBackend(ABC):

    @abstractmethod
    async def get(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    async def set(self, key: str, value: Any, ex: Union[int, datetime, None]):
        raise NotImplementedError()

    @abstractmethod
    async def update(self, key: str, value: Any):
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError()
