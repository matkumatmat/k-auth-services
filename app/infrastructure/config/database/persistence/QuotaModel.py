from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class QuotaModel(BaseModel):
    __tablename__ = "quotas"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    service_name = Column(String(100), nullable=False)
    quota_type = Column(String(100), nullable=False)
    current_usage = Column(Integer, server_default=text("0"), nullable=False)
    limit = Column(Integer, nullable=False)
    reset_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("UserModel", back_populates="quotas")

    __table_args__ = (
        Index("idx_quota_user_service", "user_id", "service_name", "quota_type", unique=True),
    )
