import json

from typing import Any
from abc import ABC, abstractmethod


class BaseEncoding(ABC):

    @staticmethod
    @abstractmethod
    def loads(data: str) -> Any:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def dumps(data: Any) -> str:
        raise NotImplementedError()


class JsonEncoding(BaseEncoding):

    @staticmethod
    def loads(data: str) -> Any:
        return json.loads(data)

    @staticmethod
    def dumps(data: Any) -> str:
        return json.dumps(data).encode()
