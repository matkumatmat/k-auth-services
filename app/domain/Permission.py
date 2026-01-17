from dataclasses import dataclass
from uuid import UUID


@dataclass
class Permission:
    id: UUID
    name: str
    resource: str
    action: str
    description: str

    def matches(self, resource: str, action: str) -> bool:
        return self.resource == resource and self.action == action

    def get_full_name(self) -> str:
        return f"{self.action}:{self.resource}"
