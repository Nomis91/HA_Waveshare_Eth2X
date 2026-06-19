"""Init file for devices module."""

from .base import BaseDevice, RegisterDef
from .deye_hybrid_gw4137 import DeyeHybridGW4137
from .deye_sun_12k import DeyeSun12K
from .deye_sun_6k import DeyeSun6K
from .deye_sun_8k import DeyeSun8K
from .generic_modbus import GenericModbusDevice
from .registry import DeviceDiscovery, DeviceRegistry

# Register all device types
DeviceRegistry.register("DEYE_SUN_12K", DeyeSun12K)
DeviceRegistry.register("DEYE_SUN_8K", DeyeSun8K)
DeviceRegistry.register("DEYE_SUN_6K", DeyeSun6K)
DeviceRegistry.register("DEYE_HYBRID_GW4137", DeyeHybridGW4137)
DeviceRegistry.register("GENERIC_MODBUS", GenericModbusDevice)

__all__ = [
    "BaseDevice",
    "RegisterDef",
    "DeyeSun12K",
    "DeyeSun8K",
    "DeyeSun6K",
    "DeyeHybridGW4137",
    "GenericModbusDevice",
    "DeviceRegistry",
    "DeviceDiscovery",
]
