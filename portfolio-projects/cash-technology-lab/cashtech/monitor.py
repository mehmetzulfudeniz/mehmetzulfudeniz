from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import DeviceHealth


@dataclass(frozen=True)
class FleetKpi:
    device_count: int
    online_count: int
    offline_count: int
    processed_total: int
    reject_total: int
    reject_rate: float
    service_due_count: int
    alerts: tuple[str, ...]


def calculate_fleet_kpi(devices: Iterable[DeviceHealth]) -> FleetKpi:
    items = list(devices)
    processed = sum(item.processed_total for item in items)
    rejected = sum(item.reject_total for item in items)
    online = sum(1 for item in items if item.online)
    alerts: list[str] = []

    for item in items:
        if not item.online:
            alerts.append(f"{item.device_id}: offline")
        if item.service_due:
            alerts.append(f"{item.device_id}: preventive service due")
        if item.temperature_c >= 55:
            alerts.append(f"{item.device_id}: high temperature ({item.temperature_c:.1f}C)")
        if item.reject_rate >= 0.05 and item.processed_total >= 100:
            alerts.append(f"{item.device_id}: elevated reject rate ({item.reject_rate:.1%})")
        if item.last_error:
            alerts.append(f"{item.device_id}: {item.last_error}")

    return FleetKpi(
        device_count=len(items),
        online_count=online,
        offline_count=len(items) - online,
        processed_total=processed,
        reject_total=rejected,
        reject_rate=0.0 if processed == 0 else rejected / processed,
        service_due_count=sum(1 for item in items if item.service_due),
        alerts=tuple(alerts),
    )
