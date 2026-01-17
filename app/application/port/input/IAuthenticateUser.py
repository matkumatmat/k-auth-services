from abc import ABC, abstractmethod

from app.application.dto.AuthenticationDTO import AuthenticationRequest, AuthenticationResult


class IAuthenticateUser(ABC):
    @abstractmethod
    async def execute_with_email(self, email: str, password: str, device_info: str, ip_address: str) -> AuthenticationResult:
        pass

    @abstractmethod
    async def execute_with_phone(self, phone: str, otp_code: str, device_info: str, ip_address: str) -> AuthenticationResult:
        pass

    @abstractmethod
    async def execute_with_oauth2(self, provider: str, code: str, device_info: str, ip_address: str) -> AuthenticationResult:
        pass
