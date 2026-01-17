from sqlalchemy import JSON, Column, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class UserBehaviorLogModel(BaseModel):
    __tablename__ = "user_behavior_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    service_name = Column(String(100), nullable=True)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(String(500), nullable=False)
    device_fingerprint = Column(String(255), nullable=True)
    geolocation = Column(JSON, nullable=True)
    additional_metadata = Column(JSON, nullable=True)

    __table_args__ = (
        Index("idx_behavior_log_user_time", "user_id", "created_at"),
        Index("idx_behavior_log_action_time", "action", "created_at"),
    )
