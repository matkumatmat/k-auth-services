from sqlalchemy import JSON, Column, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class ExternalTransactionLogModel(BaseModel):
    __tablename__ = "external_transaction_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    external_service = Column(String(100), nullable=False)
    request_type = Column(String(100), nullable=False)
    request_payload = Column(JSON, nullable=False)
    response_status = Column(Integer, nullable=False)
    response_body = Column(JSON, nullable=True)
    duration_ms = Column(Integer, nullable=False)
    idempotency_key = Column(String(255), nullable=True, index=True)
    error_message = Column(String(1000), nullable=True)

    __table_args__ = (
        Index("idx_external_log_service_time", "external_service", "created_at"),
        Index("idx_external_log_status", "response_status", "created_at"),
    )
