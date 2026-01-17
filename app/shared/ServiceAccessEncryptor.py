import hashlib
import json
from abc import ABC, abstractmethod
from typing import Protocol
from uuid import UUID

from app.shared.Cryptography import IEncryptor
from app.shared.Exceptions import DecryptionException, EncryptionException


class ServiceAccessEncryptorProtocol(Protocol):
    def encrypt_service_list(self, services: list[str], user_id: UUID) -> str:
        ...

    def decrypt_service_list(self, encrypted: str, user_id: UUID) -> list[str]:
        ...

    def hash_service_list(self, services: list[str], user_id: UUID) -> str:
        ...

    def verify_service_hash(self, services: list[str], user_id: UUID, hash_value: str) -> bool:
        ...


class IServiceAccessEncryptor(ABC):
    @abstractmethod
    def encrypt_service_list(self, services: list[str], user_id: UUID) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt_service_list(self, encrypted: str, user_id: UUID) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def hash_service_list(self, services: list[str], user_id: UUID) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_service_hash(self, services: list[str], user_id: UUID, hash_value: str) -> bool:
        raise NotImplementedError


class ServiceAccessEncryptor(IServiceAccessEncryptor):
    def __init__(self, encryptor: IEncryptor, salt: str):
        self._encryptor = encryptor
        self._salt = salt.encode()

    def _create_user_salt(self, user_id: UUID) -> bytes:
        return hashlib.sha256(str(user_id).encode() + self._salt).digest()

    def encrypt_service_list(self, services: list[str], user_id: UUID) -> str:
        try:
            sorted_services = sorted(services)
            user_salt = self._create_user_salt(user_id)
            payload = json.dumps(sorted_services)
            salted_payload = user_salt.hex() + ":" + payload
            encrypted = self._encryptor.encrypt(salted_payload)
            return encrypted
        except Exception as e:
            raise EncryptionException(
                message="Failed to encrypt service list",
                details={"user_id": str(user_id), "error": str(e)}
            )

    def decrypt_service_list(self, encrypted: str, user_id: UUID) -> list[str]:
        try:
            decrypted = self._encryptor.decrypt(encrypted)
            expected_salt = self._create_user_salt(user_id)

            parts = decrypted.split(":", 1)
            if len(parts) != 2:
                raise DecryptionException(message="Invalid encrypted format")

            salt_hex, payload = parts
            if salt_hex != expected_salt.hex():
                raise DecryptionException(
                    message="Salt mismatch - encrypted data not for this user",
                    details={"user_id": str(user_id)}
                )

            services = json.loads(payload)
            return services
        except DecryptionException:
            raise
        except Exception as e:
            raise DecryptionException(
                message="Failed to decrypt service list",
                details={"user_id": str(user_id), "error": str(e)}
            )

    def hash_service_list(self, services: list[str], user_id: UUID) -> str:
        sorted_services = sorted(services)
        user_salt = self._create_user_salt(user_id)
        payload = json.dumps(sorted_services).encode()
        hash_input = user_salt + payload + self._salt
        return hashlib.sha256(hash_input).hexdigest()

    def verify_service_hash(self, services: list[str], user_id: UUID, hash_value: str) -> bool:
        computed_hash = self.hash_service_list(services, user_id)
        return computed_hash == hash_value
