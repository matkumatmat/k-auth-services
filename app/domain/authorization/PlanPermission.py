from dataclasses import dataclass
from uuid import UUID


@dataclass
class PlanPermission:
    plan_id: UUID
    permission_id: UUID
