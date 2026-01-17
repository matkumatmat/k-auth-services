from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.domain.ValueObjects import UserPlanStatus
from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class UserPlanModel(BaseModel):
    __tablename__ = "user_plans"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(UserPlanStatus), server_default=text("'ACTIVE'"), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    auto_renew = Column(Boolean, server_default=text("false"), nullable=False)
    payment_gateway = Column(String(50), nullable=True)
    payment_gateway_subscription_id = Column(String(255), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("UserModel", back_populates="user_plans")
    plan = relationship("PlanModel", back_populates="user_plans")

    __table_args__ = (
        Index("idx_userplan_user_active", "user_id", "status"),
    )
