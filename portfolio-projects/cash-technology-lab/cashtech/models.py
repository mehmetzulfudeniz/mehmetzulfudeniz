from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


class ProcessingMode(str, Enum):
    COUNT = "count"
    DENOMINATION = "denomination"
    FITNESS = "fitness"
    ORIENTATION = "orientation"
    SERIAL_CAPTURE = "serial_capture"


class NoteDisposition(str, Enum):
    ACCEPTED = "accepted"
    REJECTED_AUTH = "rejected_auth"
    REJECTED_FITNESS = "rejected_fitness"
    REJECTED_UNSUPPORTED = "rejected_unsupported"


@dataclass(frozen=True)
class Banknote:
    currency: str
    denomination: int
    serial_number: str
    authentic: bool = True
    fit: bool = True
    orientation: str = "face_up"
    series: str = "current"


@dataclass(frozen=True)
class ProcessedNote:
    note: Banknote
    disposition: NoteDisposition
    output: str
    reason: str = ""


@dataclass
class ProcessingSummary:
    device_profile: str
    mode: ProcessingMode
    input_count: int = 0
    accepted_count: int = 0
    rejected_count: int = 0
    accepted_value: int = 0
    denomination_counts: Dict[int, int] = field(default_factory=dict)
    rejects_by_reason: Dict[str, int] = field(default_factory=dict)
    outputs: Dict[str, int] = field(default_factory=dict)
    serials: list[str] = field(default_factory=list)

    @property
    def reject_rate(self) -> float:
        return 0.0 if self.input_count == 0 else self.rejected_count / self.input_count


@dataclass(frozen=True)
class DeviceHealth:
    device_id: str
    online: bool
    temperature_c: float
    processed_total: int
    reject_total: int
    service_due: bool = False
    last_error: Optional[str] = None

    @property
    def reject_rate(self) -> float:
        return 0.0 if self.processed_total == 0 else self.reject_total / self.processed_total
