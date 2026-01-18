from app.domain.OtpCode import OtpCode
from app.domain.ValueObjects import OtpPurpose
from app.infrastructure.config.database.persistence.OtpCodeModel import OtpCodeModel


class OtpCodeMapper:
    @staticmethod
    def to_domain(model: OtpCodeModel) -> OtpCode:
        return OtpCode(
            id=model.id,
            target=model.target,
            code_hash=model.code_hash,
            purpose=OtpPurpose(model.purpose),
            is_used=model.is_used,
            expires_at=model.expires_at,
            created_at=model.created_at
        )

    @staticmethod
    def to_persistence(domain: OtpCode) -> OtpCodeModel:
        return OtpCodeModel(
            id=domain.id,
            target=domain.target,
            code_hash=domain.code_hash,
            purpose=domain.purpose.value,
            is_used=domain.is_used,
            expires_at=domain.expires_at,
            created_at=domain.created_at
        )
