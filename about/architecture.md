project : **Scallable-auth services for multi microservices**
architecture : **Layered Hexagonal pattern**
stack : **modern FastApi**
system API : **REST API**
OS and Kernel for server : **Linux and Linux Distro's**

# Company Information
Company adalah sebuah platform penyedia berbagai services, perusahaan bergerak di bidang penyedia layanan. sistem yang di gunakan adalah microservices dengan memecah beberapa service yang perusahaan miliki, perusahaan tidak berfokus kepada satu niche service dan perusahaan tidak membangun monolith sistem.
untuk saat ini ada 10 existing service yang di pegang perusahaan diantara beberapa contohnya [3dbinpacking,cvmaker,jobportal,media_information,etc]

# Architecture
# 1. base information
environtment manager : poetry
linter : ruff linter
sql database : postgresql
no-sql database : redis
stack : FastApi
ORM : SQLAlchemy
validator : pydantic
logging : structlog
testing : pytest
payment-gateaway : undefined (belum di tentukan)

# 2. company code rules
1. Strict OOP = True
2. strict hexagonal and files placements, strictly to maximizing using project structures. example: where files was domain logic must saved on domain with separately
3. modularity is greatness.
4. clean code = true 
5. separate logic with schema/interface with right placing
6. Strict use DI (dependency Injection).
7. file naming use camelcase (example: PaymentGateaway)
8. Function naming use snake case (example: payment_user)
9. Strict clean no Emoji = True
10. Srict Use custom module on shared folders if not exists, the module must created on shared/ (example: exceptions, UUID, logging)
11. strict use env/ on development or when production never hardcode anything
12. when must create documentation or plan, must created on md/ not on app/ 
13. clean code without docstring on anything code.
14. testing is run or maked when the codes was finals, not every create code must test, just test when instructed.

# 3. project structure
.
├── application/
│   ├── port/
│   │   ├── input/
│   │   └── output/
│   └── service/
├── domain/
├── env/
│   ├── .env.development
│   └── .env.production
├── infrastructure/
│   ├── adapter/
│   │   ├── input/
│   │   └── output/
│   └── config/
│       ├── database/
│       │   ├── supabase/
│       │   ├── persistence/
│       │   └── redis/
│       └── server/
├── main.py
├── shared/
└── tests/
    ├── e2e/
    ├── integration/
    └── unit/

# 4. DO and Donts
# Do 
1. always strict with company rules (point 2) 
3. always ensure to check the shared/ modules, to check the custom of company modules instead create new code and hardcode anything
2. use dict, list, | instead of deprecated code like Dict, List, Optional

# Dont's
1. never use deprecated code like using Dict, List, or Optional


# 5. type of user plan
user can choose to use shared plan. or tenancy plan.

1. Anonym-plan(unregistered) : limit 1/day access per services
1. Free-plan : limited access API, or requests. 50/day global services
2. Pro-Plan : more access from free API, or requests 1000/day
3. Enterprise-plan : more access more custom must private contact

1. company to choose gathering matrix data like what user been search, what user need, on free-plan and anonym-plan company choose to gathering more matrix like users region and more the data must anonym used for matrix and analysis for future need.
2. enterprise-plan more privately.







