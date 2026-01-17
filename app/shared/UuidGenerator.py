from abc import ABC, abstractmethod
from typing import Protocol
from uuid import UUID, uuid4


class UuidGeneratorProtocol(Protocol):
    def generate(self) -> UUID:
        ...

    def generate_str(self) -> str:
        ...


class IUuidGenerator(ABC):
    @abstractmethod
    def generate(self) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def generate_str(self) -> str:
        raise NotImplementedError


class UuidGenerator(IUuidGenerator):
    def generate(self) -> UUID:
        return uuid4()

    def generate_str(self) -> str:
        return str(self.generate())
