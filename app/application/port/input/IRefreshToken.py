from abc import ABC, abstractmethod

from app.application.dto.AuthenticationDTO import AuthenticationResult


class IRefreshToken(ABC):
    @abstractmethod
    async def execute(self, refresh_token: str) -> AuthenticationResult:
        pass
