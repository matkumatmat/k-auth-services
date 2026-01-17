from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class ApiKeyModel(BaseModel):
    __tablename__ = "api_keys"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    key_hash = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    scopes = Column(JSON, server_default=text("'[]'"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, server_default=text("true"), nullable=False)

    user = relationship("UserModel", back_populates="api_keys")

    __table_args__ = (
        Index("idx_apikey_user_active", "user_id", "is_active"),
        Index("idx_apikey_hash_active", "key_hash", postgresql_where=(is_active == True)),
    )
