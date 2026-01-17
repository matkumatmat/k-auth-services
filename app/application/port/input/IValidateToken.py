from abc import ABC, abstractmethod

from app.application.dto.TokenValidationDTO import TokenValidationResult


class IValidateToken(ABC):
    @abstractmethod
    async def execute(self, token: str) -> TokenValidationResult:
        pass
