from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceProfile:
    key: str
    display_name: str
    max_notes_per_minute: int
    output_stackers: int
    reject_stackers: int
    multi_currency: bool
    fitness_sorting: bool
    serial_number_reading: bool
    notes: str = ""


# Public capability profiles used only for simulation and portfolio learning.
# No proprietary communication protocol or firmware behavior is represented.
DEVICE_PROFILES: dict[str, DeviceProfile] = {
    "bps-c1": DeviceProfile(
        key="bps-c1",
        display_name="G+D BPS C1 (public-spec simulation profile)",
        max_notes_per_minute=1300,
        output_stackers=1,
        reject_stackers=1,
        multi_currency=True,
        fitness_sorting=True,
        serial_number_reading=True,
        notes="Compact 2-stacker profile; public product information states up to 1,300 notes/min.",
    ),
    "bps-c2-4": DeviceProfile(
        key="bps-c2-4",
        display_name="G+D BPS C2-4 evo (public-spec simulation profile)",
        max_notes_per_minute=1050,
        output_stackers=4,
        reject_stackers=1,
        multi_currency=True,
        fitness_sorting=True,
        serial_number_reading=False,
        notes="Four output compartments plus reject; public product information states 1,050 notes/min.",
    ),
    "bps-c6": DeviceProfile(
        key="bps-c6",
        display_name="G+D BPS C6 (public-spec simulation profile)",
        max_notes_per_minute=1200,
        output_stackers=20,
        reject_stackers=1,
        multi_currency=True,
        fitness_sorting=True,
        serial_number_reading=True,
        notes="Public product information states up to 72,000 notes/hour and up to 20 output stackers.",
    ),
    "bps-m3": DeviceProfile(
        key="bps-m3",
        display_name="G+D BPS M3 / M evo (public-spec simulation profile)",
        max_notes_per_minute=1266,
        output_stackers=10,
        reject_stackers=1,
        multi_currency=True,
        fitness_sorting=True,
        serial_number_reading=True,
        notes="High-speed profile based on the public 76,000 notes/hour figure.",
    ),
    "bps-m5": DeviceProfile(
        key="bps-m5",
        display_name="G+D BPS M5 / M evo (public-spec simulation profile)",
        max_notes_per_minute=2000,
        output_stackers=10,
        reject_stackers=1,
        multi_currency=True,
        fitness_sorting=True,
        serial_number_reading=True,
        notes="High-speed profile based on the public 120,000 notes/hour figure.",
    ),
    "bps-m7": DeviceProfile(
        key="bps-m7",
        display_name="G+D BPS M7 / M evo (public-spec simulation profile)",
        max_notes_per_minute=2000,
        output_stackers=10,
        reject_stackers=1,
        multi_currency=True,
        fitness_sorting=True,
        serial_number_reading=True,
        notes="Central-bank high-speed profile based on the public 120,000 notes/hour figure.",
    ),
}
