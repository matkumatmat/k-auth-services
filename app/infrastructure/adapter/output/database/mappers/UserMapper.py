from app.domain.authentication.User import User
from app.infrastructure.config.database.persistence.UserModel import UserModel


class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            phone=model.phone,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )

    @staticmethod
    def to_persistence(domain: User) -> UserModel:
        return UserModel(
            id=domain.id,
            email=domain.email,
            phone=domain.phone,
            password_hash=domain.password_hash,
            is_active=domain.is_active,
            is_verified=domain.is_verified,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            deleted_at=domain.deleted_at,
        )
