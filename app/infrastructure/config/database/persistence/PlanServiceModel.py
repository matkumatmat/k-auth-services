from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class PlanServiceModel(BaseModel):
    __tablename__ = "plan_services"
    __table_args__ = (
        UniqueConstraint('plan_id', 'service_id', name='uq_plan_service'),
    )

    id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True)
    plan_id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey('plans.id', ondelete='CASCADE'), nullable=False, index=True)
    service_id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey('services.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
