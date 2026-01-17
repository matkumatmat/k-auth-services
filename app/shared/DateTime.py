from abc import ABC, abstractmethod
from datetime import UTC, datetime, timedelta, timezone
from typing import Protocol


class DateTimeProtocol(Protocol):
    def now_utc(self) -> datetime:
        ...

    def now_local(self, tz_offset: int) -> datetime:
        ...

    def add_timedelta(self, dt: datetime, delta: timedelta) -> datetime:
        ...

    def to_timestamp(self, dt: datetime) -> int:
        ...

    def from_timestamp(self, timestamp: int) -> datetime:
        ...

    def to_iso_string(self, dt: datetime) -> str:
        ...

    def from_iso_string(self, iso_string: str) -> datetime:
        ...

    def format_datetime(self, dt: datetime, format_str: str) -> str:
        ...

    def parse_datetime(self, date_string: str, format_str: str) -> datetime:
        ...


class IDateTime(ABC):
    @abstractmethod
    def now_utc(self) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def now_local(self, tz_offset: int) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def add_timedelta(self, dt: datetime, delta: timedelta) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def to_timestamp(self, dt: datetime) -> int:
        raise NotImplementedError

    @abstractmethod
    def from_timestamp(self, timestamp: int) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def to_iso_string(self, dt: datetime) -> str:
        raise NotImplementedError

    @abstractmethod
    def from_iso_string(self, iso_string: str) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def format_datetime(self, dt: datetime, format_str: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_datetime(self, date_string: str, format_str: str) -> datetime:
        raise NotImplementedError


class DateTimeConverter(IDateTime):
    def now_utc(self) -> datetime:
        return datetime.now(UTC)

    def now_local(self, tz_offset: int) -> datetime:
        tz = timezone(timedelta(hours=tz_offset))
        return datetime.now(tz)

    def add_timedelta(self, dt: datetime, delta: timedelta) -> datetime:
        return dt + delta

    def to_timestamp(self, dt: datetime) -> int:
        return int(dt.timestamp())

    def from_timestamp(self, timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp, tz=UTC)

    def to_iso_string(self, dt: datetime) -> str:
        return dt.isoformat()

    def from_iso_string(self, iso_string: str) -> datetime:
        return datetime.fromisoformat(iso_string)

    def format_datetime(self, dt: datetime, format_str: str) -> str:
        return dt.strftime(format_str)

    def parse_datetime(self, date_string: str, format_str: str) -> datetime:
        return datetime.strptime(date_string, format_str)
