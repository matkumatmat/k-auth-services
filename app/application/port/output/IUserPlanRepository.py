from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.authentication.UserPlan import UserPlan


class IUserPlanRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_plan_id: UUID) -> UserPlan | None:
        pass

    @abstractmethod
    async def find_active_by_user(self, user_id: UUID) -> UserPlan | None:
        pass

    @abstractmethod
    async def save(self, user_plan: UserPlan) -> UserPlan:
        pass

    @abstractmethod
    async def update(self, user_plan: UserPlan) -> UserPlan:
        pass
