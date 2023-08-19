from abc import ABC, abstractmethod


class BaseTelVerifier(ABC):

    @abstractmethod
    def verify(self, tel: str, code: str| None = None) -> str:
        pass