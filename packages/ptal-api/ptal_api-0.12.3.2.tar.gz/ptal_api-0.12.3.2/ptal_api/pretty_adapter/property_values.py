from dataclasses import dataclass
from typing import Dict, Optional, Union

from .object_types import ComponentValueType


@dataclass
class LinkValue:
    link: str


@dataclass
class Date:
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


@dataclass
class Time:
    hour: int
    minute: int
    second: int


@dataclass
class DateTime:
    date: Date
    time: Optional[Time] = None


CompositeValueType = Dict[ComponentValueType, Union[str, int, float, DateTime, LinkValue]]
Value = Union[str, int, float, DateTime, LinkValue, CompositeValueType]
