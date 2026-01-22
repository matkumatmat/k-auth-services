from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.ISessionRepository import ISessionRepository
from app.domain.authorization.Session import Session
from app.infrastructure.adapter.output.database.mappers.SessionMapper import SessionMapper
from app.infrastructure.config.database.persistence.SessionModel import SessionModel
from app.shared.DateTime import DateTimeProtocol


class SessionRepository(ISessionRepository):

    def __init__(self, session: AsyncSession, datetime_converter: DateTimeProtocol):
        self._session = session
        self._mapper = SessionMapper()
        self._datetime_converter = datetime_converter

    async def find_by_id(self, session_id: UUID) -> Session | None:
        stmt = select(SessionModel).where(SessionModel.id == session_id)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def find_active_by_user(self, user_id: UUID) -> list[Session]:
        current_time = self._datetime_converter.now_utc()
        stmt = select(SessionModel).where(
            SessionModel.user_id == user_id,
            SessionModel.revoked_at.is_(None),
            SessionModel.expires_at > current_time,
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_domain(model) for model in models]

    async def save(self, session: Session) -> Session:
        session_model = self._mapper.to_persistence(session)
        self._session.add(session_model)
        await self._session.flush()
        await self._session.refresh(session_model)
        return self._mapper.to_domain(session_model)

    async def revoke(self, session_id: UUID) -> None:
        stmt = (
            update(SessionModel)
            .where(SessionModel.id == session_id)
            .values(revoked_at=self._datetime_converter.now_utc())
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def revoke_all_by_user(self, user_id: UUID) -> None:
        stmt = (
            update(SessionModel)
            .where(SessionModel.user_id == user_id)
            .values(revoked_at=self._datetime_converter.now_utc())
        )
        await self._session.execute(stmt)
        await self._session.flush()
