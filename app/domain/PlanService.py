from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class PlanService:
    id: UUID
    plan_id: UUID
    service_id: UUID
    created_at: datetime

    def belongs_to_plan(self, plan_id: UUID) -> bool:
        return self.plan_id == plan_id

    def grants_access_to_service(self, service_id: UUID) -> bool:
        return self.service_id == service_id
