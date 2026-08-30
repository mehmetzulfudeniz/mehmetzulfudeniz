from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class AuditRecord:
    sequence: int
    timestamp: str
    event: str
    payload: dict[str, Any]
    previous_hash: str
    hash: str


class TamperEvidentAuditLog:
    """Small append-only SHA-256 chained audit log for cash operations."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: str, payload: dict[str, Any]) -> AuditRecord:
        records = list(self.read_all())
        sequence = len(records) + 1
        previous_hash = records[-1].hash if records else "GENESIS"
        timestamp = datetime.now(timezone.utc).isoformat()
        digest = self._digest(sequence, timestamp, event, payload, previous_hash)
        record = AuditRecord(sequence, timestamp, event, payload, previous_hash, digest)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")
        return record

    def read_all(self) -> Iterable[AuditRecord]:
        if not self.path.exists():
            return []
        records: list[AuditRecord] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    records.append(AuditRecord(**json.loads(line)))
        return records

    def verify(self) -> bool:
        previous_hash = "GENESIS"
        for expected_sequence, record in enumerate(self.read_all(), start=1):
            if record.sequence != expected_sequence or record.previous_hash != previous_hash:
                return False
            expected = self._digest(
                record.sequence,
                record.timestamp,
                record.event,
                record.payload,
                record.previous_hash,
            )
            if record.hash != expected:
                return False
            previous_hash = record.hash
        return True

    @staticmethod
    def _digest(sequence: int, timestamp: str, event: str, payload: dict[str, Any], previous_hash: str) -> str:
        canonical = json.dumps(
            {
                "sequence": sequence,
                "timestamp": timestamp,
                "event": event,
                "payload": payload,
                "previous_hash": previous_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
