from app.application.port.input.IRegisterUser import IRegisterUser
from app.application.port.output.IUserRepository import IUserRepository
from app.domain.User import User
from app.shared.Cryptography import ISalter
from app.shared.UuidGenerator import UuidGenerator
from app.shared.Exceptions import UserAlreadyExistsException


class RegisterUserUseCase(IRegisterUser):

    def __init__(
        self, 
        user_repository: IUserRepository,
        salter: ISalter,
        uuid_generator: UuidGenerator
    ):
        self._user_repository = user_repository
        self._salter = salter
        self._uuid_generator = uuid_generator

    async def execute_with_email(self, email: str, password: str) -> User:
        existing_user = await self._user_repository.find_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(f"User with email {email} already exists.")

        password_hash = self._salter.hash_password(password)
        user_id = self._uuid_generator.generate()

        user = User(
            id=user_id,
            email=email,
            phone=None,
            password_hash=password_hash,
            is_active=False,  # User must verify email
            is_verified=False,
            created_at=None,
            updated_at=None,
        )
        return await self._user_repository.save(user)

    async def execute_with_phone(self, phone: str) -> User:
        raise NotImplementedError

    async def verify_email(self, user_id: str, otp_code: str) -> bool:
        raise NotImplementedError

    async def verify_phone(self, user_id: str, otp_code: str) -> bool:
        raise NotImplementedError
