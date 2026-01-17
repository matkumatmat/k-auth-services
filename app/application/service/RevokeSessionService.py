from uuid import UUID

from app.application.port.input.IRevokeSession import IRevokeSession
from app.application.port.output.ISessionRepository import ISessionRepository
from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.domain.UserBehaviorLog import UserBehaviorLog
from app.domain.ValueObjects import UserBehaviorAction
from app.shared.DateTime import DateTimeProtocol
from app.shared.UuidGenerator import UuidGeneratorProtocol


class RevokeSessionService(IRevokeSession):
    def __init__(
        self,
        session_repository: ISessionRepository,
        transaction_logger: ITransactionLogger,
        uuid_generator: UuidGeneratorProtocol,
        datetime_converter: DateTimeProtocol,
    ):
        self.session_repository = session_repository
        self.transaction_logger = transaction_logger
        self.uuid_generator = uuid_generator
        self.datetime_converter = datetime_converter

    async def execute(self, session_id: UUID) -> None:
        session = await self.session_repository.find_by_id(session_id)

        await self.session_repository.revoke(session_id)

        if session:
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=session.user_id,
                    action=UserBehaviorAction.LOGOUT,
                    ip_address=session.ip_address,
                    user_agent=session.device_info,
                    metadata={"session_id": str(session_id)},
                    timestamp=self.datetime_converter.now_utc()
                )
            )

    async def execute_all_by_user(self, user_id: UUID) -> None:
        await self.session_repository.revoke_all_by_user(user_id)

        await self.transaction_logger.log_user_behavior(
            UserBehaviorLog(
                id=self.uuid_generator.generate(),
                user_id=user_id,
                action=UserBehaviorAction.LOGOUT,
                ip_address="unknown",
                user_agent="logout_all_sessions",
                metadata={"action": "logout_all"},
                timestamp=self.datetime_converter.now_utc()
            )
        )
