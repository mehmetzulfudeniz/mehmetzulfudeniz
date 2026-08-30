from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict

from cashtech.audit import TamperEvidentAuditLog
from cashtech.engine import CashProcessor
from cashtech.gateway import CashDeviceGateway, LoopbackTransport
from cashtech.models import Banknote, ProcessingMode
from cashtech.monitor import calculate_fleet_kpi
from cashtech.profiles import DEVICE_PROFILES


TRY_DENOMINATIONS = [5, 10, 20, 50, 100, 200]


def generate_notes(count: int, seed: int) -> list[Banknote]:
    rng = random.Random(seed)
    notes: list[Banknote] = []
    for index in range(count):
        notes.append(
            Banknote(
                currency="TRY",
                denomination=rng.choice(TRY_DENOMINATIONS),
                serial_number=f"TR{seed:04d}{index:08d}",
                authentic=rng.random() > 0.015,
                fit=rng.random() > 0.06,
                orientation=rng.choice(["face_up", "face_down", "reverse_up", "reverse_down"]),
            )
        )
    return notes


def main() -> None:
    parser = argparse.ArgumentParser(description="Independent cash-processing simulation lab")
    parser.add_argument("--profile", choices=sorted(DEVICE_PROFILES), default="bps-c1")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mode", choices=[mode.value for mode in ProcessingMode], default="denomination")
    parser.add_argument("--audit", default=".runtime/audit.jsonl")
    args = parser.parse_args()

    notes = generate_notes(max(0, args.count), args.seed)
    gateway = CashDeviceGateway(LoopbackTransport(device_id="SIM-CASH-01"))
    gateway.submit_batch(notes)
    health = gateway.heartbeat()

    processor = CashProcessor(DEVICE_PROFILES[args.profile])
    _, summary = processor.process(notes, ProcessingMode(args.mode))

    audit = TamperEvidentAuditLog(args.audit)
    audit.append(
        "processing_session_completed",
        {
            "profile": args.profile,
            "mode": args.mode,
            "input_count": summary.input_count,
            "accepted_count": summary.accepted_count,
            "rejected_count": summary.rejected_count,
            "accepted_value": summary.accepted_value,
        },
    )

    fleet = calculate_fleet_kpi([health])
    output = {
        "summary": asdict(summary),
        "device_health": asdict(health),
        "fleet_kpi": asdict(fleet),
        "audit_chain_valid": audit.verify(),
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
