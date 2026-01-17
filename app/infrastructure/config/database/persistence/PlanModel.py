from sqlalchemy import JSON, Boolean, Column, DateTime, Enum, String, text
from sqlalchemy.orm import relationship

from app.domain.ValueObjects import BillingCycle
from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class PlanModel(BaseModel):
    __tablename__ = "plans"

    name = Column(String(100), nullable=False, unique=True)
    billing_cycle = Column(Enum(BillingCycle), nullable=False)
    features = Column(JSON, server_default=text("'[]'"), nullable=False)
    rate_limits = Column(JSON, server_default=text("'{}'"), nullable=False)
    quota_limits = Column(JSON, server_default=text("'{}'"), nullable=False)
    is_active = Column(Boolean, server_default=text("true"), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    user_plans = relationship("UserPlanModel", back_populates="plan")
    plan_permissions = relationship("PlanPermissionModel", back_populates="plan", cascade="all, delete-orphan")
