from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Protocol

import jwt

from app.shared.DateTime import DateTimeProtocol
from app.shared.Exceptions import TokenExpiredException, TokenInvalidException


class TokenGeneratorProtocol(Protocol):
    def generate(self, payload: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        ...

    def decode(self, token: str) -> dict[str, Any]:
        ...

    def verify(self, token: str) -> bool:
        ...


class ITokenGenerator(ABC):
    @abstractmethod
    def generate(self, payload: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def verify(self, token: str) -> bool:
        raise NotImplementedError


class JwtTokenGenerator(ITokenGenerator):
    def __init__(self, secret_key: str, datetime_converter: DateTimeProtocol, algorithm: str = "HS256"):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._datetime = datetime_converter

    def generate(self, payload: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        to_encode = payload.copy()
        now = self._datetime.now_utc()

        if expires_delta:
            expire = self._datetime.add_timedelta(now, expires_delta)
        else:
            expire = self._datetime.add_timedelta(now, timedelta(minutes=15))

        to_encode.update({"exp": expire, "iat": now})

        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def decode(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            raise TokenInvalidException()

    def verify(self, token: str) -> bool:
        try:
            jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return True
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            return False
