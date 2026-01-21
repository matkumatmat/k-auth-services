from app.domain.authorization.Session import Session
from app.infrastructure.config.database.persistence.SessionModel import SessionModel


class SessionMapper:
    @staticmethod
    def to_domain(model: SessionModel) -> Session:
        return Session(
            id=model.id,
            user_id=model.user_id,
            refresh_token_hash=model.refresh_token_hash,
            device_info=model.device_info,
            ip_address=model.ip_address,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_persistence(domain: Session) -> SessionModel:
        return SessionModel(
            id=domain.id,
            user_id=domain.user_id,
            refresh_token_hash=domain.refresh_token_hash,
            device_info=domain.device_info,
            ip_address=domain.ip_address,
            expires_at=domain.expires_at,
            revoked_at=domain.revoked_at,
            created_at=domain.created_at,
        )
