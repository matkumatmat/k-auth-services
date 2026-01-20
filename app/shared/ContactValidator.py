import re

from app.domain.ValueObjects import AuthProviderType


class ContactTypeDetector:
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_REGEX = re.compile(r'^\+?[0-9]{10,15}$')

    @staticmethod
    def detect(contact: str) -> AuthProviderType | None:
        contact = contact.strip()

        if ContactTypeDetector.EMAIL_REGEX.match(contact):
            return AuthProviderType.EMAIL

        if ContactTypeDetector.PHONE_REGEX.match(contact):
            return AuthProviderType.WHATSAPP

        return None

    @staticmethod
    def is_email(contact: str) -> bool:
        return ContactTypeDetector.detect(contact) == AuthProviderType.EMAIL

    @staticmethod
    def is_phone(contact: str) -> bool:
        return ContactTypeDetector.detect(contact) == AuthProviderType.WHATSAPP

    @staticmethod
    def normalize_phone(phone: str) -> str:
        phone = phone.strip()
        phone = re.sub(r'\D', '', phone)

        if phone.startswith('0'):
            phone = '62' + phone[1:]
        elif not phone.startswith('62'):
            phone = '62' + phone

        return phone

    @staticmethod
    def normalize_email(email: str) -> str:
        return email.strip().lower()
