from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cashtech.audit import TamperEvidentAuditLog
from cashtech.engine import CashProcessor
from cashtech.gateway import CashDeviceGateway, LoopbackTransport
from cashtech.models import Banknote, DeviceHealth, ProcessingMode
from cashtech.monitor import calculate_fleet_kpi
from cashtech.profiles import DEVICE_PROFILES


class CashProcessorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.processor = CashProcessor(DEVICE_PROFILES["bps-c1"])

    def test_counts_value_and_denomination(self) -> None:
        notes = [
            Banknote("TRY", 100, "A1"),
            Banknote("TRY", 100, "A2"),
            Banknote("TRY", 50, "A3"),
        ]
        _, summary = self.processor.process(notes, ProcessingMode.DENOMINATION)
        self.assertEqual(summary.accepted_count, 3)
        self.assertEqual(summary.accepted_value, 250)
        self.assertEqual(summary.denomination_counts, {100: 2, 50: 1})

    def test_authentication_reject(self) -> None:
        notes = [Banknote("TRY", 200, "BAD1", authentic=False)]
        processed, summary = self.processor.process(notes)
        self.assertEqual(summary.rejected_count, 1)
        self.assertEqual(processed[0].output, "reject")
        self.assertEqual(summary.rejects_by_reason["authentication_reject"], 1)

    def test_fitness_mode_rejects_unfit_note(self) -> None:
        notes = [Banknote("TRY", 20, "WORN1", fit=False)]
        _, summary = self.processor.process(notes, ProcessingMode.FITNESS)
        self.assertEqual(summary.rejected_count, 1)
        self.assertEqual(summary.rejects_by_reason["unfit_note"], 1)

    def test_serial_capture_mode_records_serials(self) -> None:
        notes = [Banknote("TRY", 10, "SERIAL-001")]
        _, summary = self.processor.process(notes, ProcessingMode.SERIAL_CAPTURE)
        self.assertEqual(summary.serials, ["SERIAL-001"])


class GatewayAndMonitoringTests(unittest.TestCase):
    def test_loopback_gateway_health(self) -> None:
        gateway = CashDeviceGateway(LoopbackTransport("SIM-007"))
        gateway.submit_batch([Banknote("TRY", 100, "A"), Banknote("TRY", 50, "B", authentic=False)])
        health = gateway.heartbeat()
        self.assertTrue(health.online)
        self.assertEqual(health.processed_total, 2)
        self.assertEqual(health.reject_total, 1)

    def test_fleet_kpi_generates_alerts(self) -> None:
        fleet = calculate_fleet_kpi(
            [
                DeviceHealth("A", True, 40.0, 1000, 10),
                DeviceHealth("B", False, 60.0, 100, 10, service_due=True, last_error="feed jam"),
            ]
        )
        self.assertEqual(fleet.device_count, 2)
        self.assertEqual(fleet.offline_count, 1)
        self.assertGreaterEqual(len(fleet.alerts), 4)


class AuditTests(unittest.TestCase):
    def test_hash_chain_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "audit.jsonl"
            log = TamperEvidentAuditLog(path)
            log.append("session_started", {"operator": "demo"})
            log.append("session_completed", {"count": 100})
            self.assertTrue(log.verify())


if __name__ == "__main__":
    unittest.main()
