from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class PermissionModel(BaseModel):
    __tablename__ = "permissions"

    name = Column(String(100), nullable=False, unique=True)
    resource = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)

    plan_permissions = relationship("PlanPermissionModel", back_populates="permission", cascade="all, delete-orphan")
