from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def load(self, key: str, file: bytes, content_type: str) -> str:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def remove(self, link: str) -> None:
        raise NotImplementedError("Method not implemented")
