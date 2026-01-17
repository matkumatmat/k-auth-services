from dataclasses import dataclass


@dataclass
class PaginationParams:
    offset: int = 0
    limit: int = 50

    def __post_init__(self) -> None:
        if self.offset < 0:
            raise ValueError("Offset must be non-negative")
        if self.limit <= 0 or self.limit > 1000:
            raise ValueError("Limit must be between 1 and 1000")


@dataclass
class PaginatedResult[T]:
    items: list[T]
    total_count: int
    offset: int
    limit: int

    @property
    def has_more(self) -> bool:
        return (self.offset + self.limit) < self.total_count
