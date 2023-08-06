from enum import Enum
from cpt_python.bluetooth_data.virtual_sensors import *


class BatteryStatus(Enum):
    ok = 0x00
    low = 0x01


class BatteryStatusVirtualSensors:
    battery_status: BatteryStatus
    virtual_sensors: VirtualSensors

    __VIRTUAL_SENSORS_SHIFT: int = 1
    __BATTERY_STATUS_MASK = 0x3

    def __init__(self, battery_status: BatteryStatus, virtual_sensors: VirtualSensors):
        self.battery_status = battery_status
        self.virtual_sensors = virtual_sensors

    @staticmethod
    def from_byte(byte: int) -> "BatteryStatusVirtualSensors":
        raw_status = (
            byte & (BatteryStatusVirtualSensors.__BATTERY_STATUS_MASK))
        battery = BatteryStatus(raw_status) or BatteryStatus.ok
        virtual_sensors = VirtualSensors.from_byte(
            byte >> BatteryStatusVirtualSensors.__VIRTUAL_SENSORS_SHIFT)

        return BatteryStatusVirtualSensors(battery_status=battery, virtual_sensors=virtual_sensors)

    @staticmethod
    def default_values() -> "BatteryStatusVirtualSensors":
        return BatteryStatusVirtualSensors(battery_status=BatteryStatus.ok,
                                           virtual_sensors=VirtualSensors(virtual_core=VirtualCoreSensor.T1, virtual_surface=VirtualSurfaceSensor.T4, virtual_ambient=VirtualAmbientSensor.T5))
