import base64
import hashlib
from abc import ABC, abstractmethod
from typing import Protocol

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

from app.shared.Exceptions import DecryptionException, EncryptionException


class SalterProtocol(Protocol):
    def hash_password(self, password: str) -> str:
        ...

    def verify_password(self, password: str, hashed_password: str) -> bool:
        ...


class ISalter(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError


class Salter(ISalter):
    def __init__(self, salt: str):
        self._salt = salt.encode()

    def hash_password(self, password: str) -> str:
        pwd_bytes = password.encode()
        hashed = hashlib.pbkdf2_hmac('sha256', pwd_bytes, self._salt, 100000)
        return base64.b64encode(hashed).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.hash_password(password) == hashed_password


class EncryptorProtocol(Protocol):
    def encrypt(self, data: str) -> str:
        ...

    def decrypt(self, encrypted_data: str) -> str:
        ...


class IEncryptor(ABC):
    @abstractmethod
    def encrypt(self, data: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, encrypted_data: str) -> str:
        raise NotImplementedError


class FernetEncryptor(IEncryptor):
    def __init__(self, encryption_key: str):
        try:
            self._fernet = Fernet(encryption_key.encode())
        except Exception as e:
            raise EncryptionException(message="Invalid encryption key", details={"error": str(e)})

    def encrypt(self, data: str) -> str:
        try:
            encrypted = self._fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            raise EncryptionException(details={"error": str(e)})

    def decrypt(self, encrypted_data: str) -> str:
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self._fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise DecryptionException(details={"error": str(e)})


class EncryptionKeyGenerator:
    @staticmethod
    def generate_key() -> str:
        return Fernet.generate_key().decode()

    @staticmethod
    def derive_key_from_password(password: str, salt: str) -> str:
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key.decode()
