from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.domain.ValueObjects import AuthProviderType
from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class AuthProviderModel(BaseModel):
    __tablename__ = "auth_providers"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_type = Column(Enum(AuthProviderType), nullable=False)
    provider_user_id = Column(String(255), nullable=False)
    is_primary = Column(Boolean, server_default=text("false"), nullable=False)
    provider_metadata = Column(JSON, server_default=text("'{}'"), nullable=False)

    user = relationship("UserModel", back_populates="auth_providers")

    __table_args__ = (
        Index("idx_auth_provider_external", "provider_type", "provider_user_id", unique=True),
    )
