from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Iterable

from .models import Banknote, DeviceHealth


class Transport(ABC):
    """Generic transport boundary for an authorized device integration.

    Real hardware adapters should be implemented only from vendor-provided,
    licensed SDK/protocol documentation. This project intentionally ships no
    reverse-engineered or proprietary G+D transport implementation.
    """

    @abstractmethod
    def request(self, payload: dict) -> dict:
        raise NotImplementedError


class LoopbackTransport(Transport):
    """Deterministic local transport used by tests and demos."""

    def __init__(self, device_id: str = "SIM-001") -> None:
        self.device_id = device_id
        self.processed_total = 0
        self.reject_total = 0

    def request(self, payload: dict) -> dict:
        command = payload.get("command")
        if command == "heartbeat":
            return {
                "device_id": self.device_id,
                "online": True,
                "temperature_c": 37.5,
                "processed_total": self.processed_total,
                "reject_total": self.reject_total,
                "service_due": False,
                "last_error": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        if command == "submit_batch":
            notes = payload.get("notes", [])
            self.processed_total += len(notes)
            self.reject_total += sum(1 for note in notes if not note.get("authentic", True))
            return {
                "accepted": True,
                "batch_size": len(notes),
                "device_id": self.device_id,
            }

        return {"accepted": False, "error": "unsupported_command"}


class CashDeviceGateway:
    """Vendor-neutral application boundary for cash-processing equipment."""

    def __init__(self, transport: Transport) -> None:
        self.transport = transport

    def heartbeat(self) -> DeviceHealth:
        response = self.transport.request({"command": "heartbeat"})
        return DeviceHealth(
            device_id=response["device_id"],
            online=bool(response["online"]),
            temperature_c=float(response["temperature_c"]),
            processed_total=int(response["processed_total"]),
            reject_total=int(response["reject_total"]),
            service_due=bool(response.get("service_due", False)),
            last_error=response.get("last_error"),
        )

    def submit_batch(self, notes: Iterable[Banknote]) -> dict:
        payload = {
            "command": "submit_batch",
            "notes": [asdict(note) for note in notes],
        }
        # Round-trip through JSON to enforce a clean serialization boundary.
        wire_payload = json.loads(json.dumps(payload))
        return self.transport.request(wire_payload)
