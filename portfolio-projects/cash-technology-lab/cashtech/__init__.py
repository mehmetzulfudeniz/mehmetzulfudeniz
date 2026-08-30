"""Independent cash-processing simulation and integration lab.

This package contains original educational code. It does not contain or
implement proprietary G+D protocols, firmware, source code, or binaries.
"""

from .engine import CashProcessor
from .models import Banknote, DeviceHealth, ProcessingMode
from .profiles import DEVICE_PROFILES, DeviceProfile

__all__ = [
    "Banknote",
    "CashProcessor",
    "DeviceHealth",
    "ProcessingMode",
    "DeviceProfile",
    "DEVICE_PROFILES",
]
