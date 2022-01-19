from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass


class DateFormat(enum.Enum):
    datetime = "%Y-%m-%dT%H:%M:%S"
    date = "%Y-%m-%d"
    gYearMonth = "%Y-%m"
    gYear = "%Y"

    def key(self):
        if self is DateFormat.datetime:
            return "gco:DateTime"
        return "gco:Date"

    def from_datetime(self, dt: datetime.date):
        return dt.strftime(self.value)


@dataclass
class DateTime:
    value: datetime.datetime
    format: DateFormat = DateFormat.datetime

    def as_bf(self):
        return {"$": self.format.from_datetime(self.value)}


@dataclass
class Date:
    value: datetime.date
    format: DateFormat = DateFormat.date

    def as_bf(self):
        return {"$": self.format.from_datetime(self.value)}


@dataclass
class TM_PeriodDuration:
    ...
