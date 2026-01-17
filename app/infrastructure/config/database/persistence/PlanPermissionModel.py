from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.config.database.persistence.BaseModel import Base


class PlanPermissionModel(Base):
    __tablename__ = "plan_permissions"

    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    plan = relationship("PlanModel", back_populates="plan_permissions")
    permission = relationship("PermissionModel", back_populates="plan_permissions")

    __table_args__ = (
        PrimaryKeyConstraint("plan_id", "permission_id"),
    )
