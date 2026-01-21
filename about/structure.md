.
├── about
│   ├── structure.json
│   └── structure.md
├── alembic
│   ├── versions
│   │   ├── b8352b457691_initial_migration_kauth_db.py
│   │   └── d2991ea69294_create_plan_services_table.py
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── app
│   ├── application
│   │   ├── dto
│   │   │   ├── AuthenticationDTO.py
│   │   │   ├── PaginationParams.py
│   │   │   ├── QuotaCheckDTO.py
│   │   │   ├── ServiceAccessDTO.py
│   │   │   └── TokenValidationDTO.py
│   │   ├── port
│   │   │   ├── input
│   │   │   │   ├── IAuthenticateUser.py
│   │   │   │   ├── ICheckQuota.py
│   │   │   │   ├── ILinkAuthProvider.py
│   │   │   │   ├── IRefreshToken.py
│   │   │   │   ├── IRegisterUser.py
│   │   │   │   ├── IResendOtp.py
│   │   │   │   ├── IRevokeSession.py
│   │   │   │   ├── IValidateServiceAccess.py
│   │   │   │   └── IValidateToken.py
│   │   │   └── output
│   │   │       ├── IApiKeyRepository.py
│   │   │       ├── IAuthProviderRepository.py
│   │   │       ├── IJwtService.py
│   │   │       ├── IOtpCodeRepository.py
│   │   │       ├── IPlanRepository.py
│   │   │       ├── IPlanServiceRepository.py
│   │   │       ├── IQuotaRepository.py
│   │   │       ├── IServiceAccessRepository.py
│   │   │       ├── IServiceRepository.py
│   │   │       ├── ISessionRepository.py
│   │   │       ├── ITransactionLogger.py
│   │   │       ├── IUserPlanRepository.py
│   │   │       └── IUserRepository.py
│   │   └── service
│   │       ├── AuthenticationService.py
│   │       ├── LinkAuthProviderService.py
│   │       ├── QuotaManagementService.py
│   │       ├── RefreshTokenService.py
│   │       ├── ResendOtpService.py
│   │       ├── RevokeSessionService.py
│   │       ├── ServiceAccessValidationService.py
│   │       ├── TokenValidationService.py
│   │       └── UserRegistrationService.py
│   ├── domain
│   │   ├── authentication
│   │   │   ├── OtpCode.py
│   │   │   ├── User.py
│   │   │   └── UserPlan.py
│   │   ├── authorization
│   │   │   ├── ApiKey.py
│   │   │   ├── AuthProvider.py
│   │   │   ├── Permission.py
│   │   │   ├── PlanPermission.py
│   │   │   ├── ServiceAccess.py
│   │   │   └── Session.py
│   │   ├── exceptions
│   │   │   ├── AuthenticationExceptions.py
│   │   │   ├── AuthorizationExceptions.py
│   │   │   ├── BaseException.py
│   │   │   ├── RateLimitExceptions.py
│   │   │   ├── UserExceptions.py
│   │   │   └── __init__.py
│   │   ├── log
│   │   │   ├── DatabaseTransactionLog.py
│   │   │   ├── ExternalTransactionLog.py
│   │   │   └── UserBehaviorLog.py
│   │   ├── service
│   │   │   ├── Plan.py
│   │   │   ├── PlanService.py
│   │   │   ├── Quota.py
│   │   │   └── Service.py
│   │   └── ValueObjects.py
│   ├── infrastructure
│   │   ├── adapter
│   │   │   ├── input
│   │   │   │   ├── http
│   │   │   │   │   ├── AuthController.py
│   │   │   │   │   ├── OtpController.py
│   │   │   │   │   ├── UserController.py
│   │   │   │   │   └── ValidationController.py
│   │   │   │   └── middleware
│   │   │   │       └── ExceptionHandler.py
│   │   │   └── output
│   │   │       ├── database
│   │   │       │   ├── mappers
│   │   │       │   │   ├── ApiKeyMapper.py
│   │   │       │   │   ├── AuthProviderMapper.py
│   │   │       │   │   ├── OtpCodeMapper.py
│   │   │       │   │   ├── PlanMapper.py
│   │   │       │   │   ├── PlanServiceMapper.py
│   │   │       │   │   ├── QuotaMapper.py
│   │   │       │   │   ├── ServiceAccessMapper.py
│   │   │       │   │   ├── ServiceMapper.py
│   │   │       │   │   ├── SessionMapper.py
│   │   │       │   │   ├── UserMapper.py
│   │   │       │   │   └── UserPlanMapper.py
│   │   │       │   └── repositories
│   │   │       │       ├── ApiKeyRepository.py
│   │   │       │       ├── AuthProviderRepository.py
│   │   │       │       ├── OtpCodeRepository.py
│   │   │       │       ├── PlanRepository.py
│   │   │       │       ├── PlanServiceRepository.py
│   │   │       │       ├── QuotaRepository.py
│   │   │       │       ├── ServiceAccessRepository.py
│   │   │       │       ├── ServiceRepository.py
│   │   │       │       ├── SessionRepository.py
│   │   │       │       ├── TransactionLoggerRepository.py
│   │   │       │       ├── UserPlanRepository.py
│   │   │       │       └── UserRepository.py
│   │   │       └── jwt
│   │   │           └── JwtService.py
│   │   ├── config
│   │   │   ├── database
│   │   │   │   ├── persistence
│   │   │   │   │   ├── ApiKeyModel.py
│   │   │   │   │   ├── AuthProviderModel.py
│   │   │   │   │   ├── BaseModel.py
│   │   │   │   │   ├── DatabaseTransactionLogModel.py
│   │   │   │   │   ├── ExternalTransactionLogModel.py
│   │   │   │   │   ├── OtpCodeModel.py
│   │   │   │   │   ├── PermissionModel.py
│   │   │   │   │   ├── PlanModel.py
│   │   │   │   │   ├── PlanPermissionModel.py
│   │   │   │   │   ├── PlanServiceModel.py
│   │   │   │   │   ├── QuotaModel.py
│   │   │   │   │   ├── ServiceAccessModel.py
│   │   │   │   │   ├── ServiceModel.py
│   │   │   │   │   ├── SessionModel.py
│   │   │   │   │   ├── UserBehaviorLogModel.py
│   │   │   │   │   ├── UserModel.py
│   │   │   │   │   ├── UserPlanModel.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── redis
│   │   │   │   │   └── RedisClient.py
│   │   │   │   ├── supabase
│   │   │   │   └── DatabaseSession.py
│   │   │   ├── server
│   │   │   │   ├── CorsMiddlewareSettings.py
│   │   │   │   └── Settings.py
│   │   │   └── EnvConfig.py
│   │   └── dependencies.py
│   ├── shared
│   │   ├── ContactValidator.py
│   │   ├── Cryptography.py
│   │   ├── DateTime.py
│   │   ├── Exceptions.py
│   │   ├── Logger.py
│   │   ├── OtpRateLimiter.py
│   │   ├── ServiceAccessEncryptor.py
│   │   ├── TokenGenerator.py
│   │   └── UuidGenerator.py
│   ├── tests
│   │   ├── e2e
│   │   │   └── ddos_test.py
│   │   ├── integration
│   │   ├── unit
│   │   │   └── __init__.py
│   │   └── __init__.py
│   └── main.py
├── docker
│   ├── fastapi
│   └── postgres
│       └── init.sql
├── scripts
│   ├── gen_structures.sh
│   ├── init_db.py
│   └── seed_database.py
├── README.md
├── alembic.ini
├── architecture.md
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── quickstart.sh
└── start_server.sh

42 directories, 144 files
