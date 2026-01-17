from sqlalchemy import Boolean, Column, DateTime, Index, String, text
from sqlalchemy.orm import relationship

from app.infrastructure.config.database.persistence.BaseModel import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(50), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, server_default=text("true"), nullable=False)
    is_verified = Column(Boolean, server_default=text("false"), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    auth_providers = relationship("AuthProviderModel", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("SessionModel", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("ApiKeyModel", back_populates="user", cascade="all, delete-orphan")
    user_plans = relationship("UserPlanModel", back_populates="user", cascade="all, delete-orphan")
    quotas = relationship("QuotaModel", back_populates="user", cascade="all, delete-orphan")
    service_accesses = relationship("ServiceAccessModel", back_populates="user", cascade="all, delete-orphan")
    otp_codes = relationship("OtpCodeModel", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_user_active", "is_active", "is_verified"),
        Index("idx_user_email_active", "email", postgresql_where=(deleted_at == None)),
        Index("idx_user_phone_active", "phone", postgresql_where=(deleted_at == None)),
    )
