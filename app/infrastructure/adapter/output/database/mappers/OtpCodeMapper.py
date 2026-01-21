from app.domain.authentication.OtpCode import OtpCode
from app.domain.ValueObjects import OtpPurpose, OtpDeliveryMethod
from app.infrastructure.config.database.persistence.OtpCodeModel import OtpCodeModel


class OtpCodeMapper:
    @staticmethod
    def to_domain(model: OtpCodeModel) -> OtpCode:
        return OtpCode(
            id=model.id,
            user_id=model.user_id,
            delivery_method=OtpDeliveryMethod(model.delivery_method), # Ditambahkan & Casting Enum
            delivery_target=model.delivery_target, # Ganti 'target' jadi 'delivery_target'
            code_hash=model.code_hash,
            purpose=OtpPurpose(model.purpose),
            used_at=model.used_at,
            expires_at=model.expires_at,
            created_at=model.created_at
        )

    @staticmethod
    def to_persistence(domain: OtpCode) -> OtpCodeModel:
        return OtpCodeModel(
            id=domain.id,
            user_id=domain.user_id,
            code_hash=domain.code_hash,
            delivery_method=domain.delivery_method,
            delivery_target=domain.delivery_target,
            purpose=domain.purpose,
            expires_at=domain.expires_at,
            used_at=domain.used_at,
            created_at=domain.created_at
        )
