from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class SessionModel(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token_hash = Column(String(255), nullable=False)
    device_info = Column(String(500), nullable=False)
    ip_address = Column(String(45), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("UserModel", back_populates="sessions")

    __table_args__ = (
        Index("idx_session_user_active", "user_id", postgresql_where=(revoked_at == None)),
        Index("idx_session_expiry_active", "expires_at", postgresql_where=(revoked_at == None)),
    )
