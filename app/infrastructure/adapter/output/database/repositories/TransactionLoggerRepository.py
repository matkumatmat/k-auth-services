from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.domain.DatabaseTransactionLog import DatabaseTransactionLog
from app.domain.ExternalTransactionLog import ExternalTransactionLog
from app.domain.UserBehaviorLog import UserBehaviorLog
from app.infrastructure.config.database.persistence.DatabaseTransactionLogModel import DatabaseTransactionLogModel
from app.infrastructure.config.database.persistence.ExternalTransactionLogModel import ExternalTransactionLogModel
from app.infrastructure.config.database.persistence.UserBehaviorLogModel import UserBehaviorLogModel


class TransactionLoggerRepository(ITransactionLogger):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def log_database_transaction(self, log: DatabaseTransactionLog) -> None:
        log_model = DatabaseTransactionLogModel(
            id=log.id,
            table_name=log.table_name,
            operation=log.operation.value,
            record_id=log.record_id,
            user_id=log.user_id,
            old_values=log.old_values,
            new_values=log.new_values,
            timestamp=log.timestamp
        )
        self._session.add(log_model)
        await self._session.flush()

    async def log_external_transaction(self, log: ExternalTransactionLog) -> None:
        log_model = ExternalTransactionLogModel(
            id=log.id,
            service_name=log.service_name,
            endpoint=log.endpoint,
            method=log.method,
            status_code=log.status_code,
            request_payload=log.request_payload,
            response_payload=log.response_payload,
            duration_ms=log.duration_ms,
            timestamp=log.timestamp
        )
        self._session.add(log_model)
        await self._session.flush()

    async def log_user_behavior(self, log: UserBehaviorLog) -> None:
        log_model = UserBehaviorLogModel(
            id=log.id,
            user_id=log.user_id,
            action=log.action.value,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            metadata=log.metadata,
            timestamp=log.timestamp
        )
        self._session.add(log_model)
        await self._session.flush()
