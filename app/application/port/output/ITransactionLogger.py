from abc import ABC, abstractmethod

from app.domain.log.DatabaseTransactionLog import DatabaseTransactionLog
from app.domain.log.ExternalTransactionLog import ExternalTransactionLog
from app.domain.log.UserBehaviorLog import UserBehaviorLog


class ITransactionLogger(ABC):
    @abstractmethod
    async def log_database_transaction(self, log: DatabaseTransactionLog) -> None:
        pass

    @abstractmethod
    async def log_external_transaction(self, log: ExternalTransactionLog) -> None:
        pass

    @abstractmethod
    async def log_user_behavior(self, log: UserBehaviorLog) -> None:
        pass
