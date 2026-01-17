from sqlalchemy import JSON, Column, Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID

from app.domain.ValueObjects import DatabaseOperation
from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class DatabaseTransactionLogModel(BaseModel):
    __tablename__ = "database_transaction_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    table_name = Column(String(100), nullable=False)
    operation = Column(Enum(DatabaseOperation), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    transaction_id = Column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (
        Index("idx_db_log_table_time", "table_name", "created_at"),
        Index("idx_db_log_transaction", "transaction_id"),
    )
