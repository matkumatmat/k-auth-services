from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.domain.ValueObjects import OtpDeliveryMethod, OtpPurpose
from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class OtpCodeModel(BaseModel):
    __tablename__ = "otp_codes"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    code_hash = Column(String(255), nullable=False)
    delivery_method = Column(Enum(OtpDeliveryMethod), nullable=False)
    delivery_target = Column(String(255), nullable=False)
    purpose = Column(Enum(OtpPurpose), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("UserModel", back_populates="otp_codes")

    __table_args__ = (
        Index("idx_otp_target_purpose", "delivery_target", "purpose", postgresql_where=(used_at == None)),
    )
