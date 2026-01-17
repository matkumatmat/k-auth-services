from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class ServiceAccessModel(BaseModel):
    __tablename__ = "service_accesses"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    service_name = Column(String(100), nullable=False)
    is_allowed = Column(Boolean, server_default=text("true"), nullable=False)
    allowed_features = Column(JSON, nullable=True)
    granted_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("UserModel", back_populates="service_accesses")

    __table_args__ = (
        Index("idx_service_access_lookup", "user_id", "service_name", postgresql_where=(is_allowed == True)),
    )
