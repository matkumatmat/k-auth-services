from enum import Enum


class AuthProviderType(str, Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    OAUTH2_GOOGLE = "oauth2_google"


class BillingCycle(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"
    CUSTOM = "custom"


class UserPlanStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class OtpDeliveryMethod(str, Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class OtpPurpose(str, Enum):
    REGISTRATION = "registration"
    LOGIN = "login"
    PASSWORD_RESET = "password_reset"


class DatabaseOperation(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class UserBehaviorAction(str, Enum):
    LOGIN_ATTEMPT = "login_attempt"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    TOKEN_REFRESH = "token_refresh"
    QUOTA_CHECK = "quota_check"
    ACCESS_DENIED = "access_denied"
    LOGOUT = "logout"
    PASSWORD_RESET_REQUEST = "password_reset_request"
    PASSWORD_RESET_SUCCESS = "password_reset_success"
