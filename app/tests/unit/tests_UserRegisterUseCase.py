import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone

from app.domain.User import User
from app.application.usecase.RegisterUserUseCase import RegisterUserUseCase
from app.application.port.output.IUserRepository import IUserRepository
from app.shared.Cryptography import Salter
from app.shared.UuidGenerator import UuidGenerator
from app.shared.Exceptions import UserAlreadyExistsException

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_user_repository():
    return AsyncMock(spec=IUserRepository)

@pytest.fixture
def mock_salter():
    mock = MagicMock(spec=Salter)
    mock.hash_password.return_value = "hashed_password"
    return mock

@pytest.fixture
def mock_uuid_generator():
    mock = MagicMock(spec=UuidGenerator)
    mock.generate.return_value = uuid4()
    return mock

@pytest.fixture
def register_user_use_case(mock_user_repository, mock_salter, mock_uuid_generator):
    return RegisterUserUseCase(
        user_repository=mock_user_repository,
        salter=mock_salter,
        uuid_generator=mock_uuid_generator
    )

async def test_register_user_success(
    register_user_use_case: RegisterUserUseCase,
    mock_user_repository: AsyncMock,
    mock_uuid_generator: MagicMock
):
    """
    Tests successful user registration when the email does not exist.
    """
    # Arrange
    email = "test@example.com"
    password = "password123"
    mock_user_repository.find_by_email.return_value = None
    
    # Mock the save to return the user passed to it
    async def save_side_effect(user: User) -> User:
        return user
    mock_user_repository.save.side_effect = save_side_effect

    # Act
    result_user = await register_user_use_case.execute_with_email(email, password)

    # Assert
    mock_user_repository.find_by_email.assert_awaited_once_with(email)
    mock_user_repository.save.assert_awaited_once()
    
    saved_user_arg = mock_user_repository.save.call_args[0][0]
    assert saved_user_arg.email == email
    assert saved_user_arg.password_hash == "hashed_password"
    assert saved_user_arg.id == mock_uuid_generator.generate.return_value
    
    assert result_user.email == email

async def test_register_user_already_exists(
    register_user_use_case: RegisterUserUseCase,
    mock_user_repository: AsyncMock
):
    """
    Tests that registration fails if the user's email already exists.
    """
    # Arrange
    email = "existing@example.com"
    password = "password123"
    existing_user_id = uuid4()
    mock_user_repository.find_by_email.return_value = User(
        id=existing_user_id, 
        email=email,
        phone=None,
        password_hash="hashed_password",
        is_active=True,
        is_verified=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # Act & Assert
    with pytest.raises(UserAlreadyExistsException, match=f"User with email {email} already exists."):
        await register_user_use_case.execute_with_email(email, password)
    
    mock_user_repository.find_by_email.assert_awaited_once_with(email)
    mock_user_repository.save.assert_not_awaited()
