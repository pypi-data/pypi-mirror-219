
from enum import Enum
from cpt_python.bluetooth_data.probe_temperatures import ProbeTemperatures
from cpt_python.bluetooth_data.mode_id import ModeId
from cpt_python.bluetooth_data.battery_status_virtual_sensors import BatteryStatusVirtualSensors

# Enumeration of Combustion, Inc. product types.


class CombustionProductType(Enum):
    unknown = 0x00
    probe = 0x01
    node = 0x02


# Struct
class AdvertisingData:
    '''Advertising data received from device.
    '''
    # Type of Combustion product
    type: CombustionProductType
    # Product serial number
    serialNumber: int
    # Latest temperatures read by device
    temperatures: ProbeTemperatures
    # ModeId (Probe color, ID, and mode)
    modeId: ModeId
    # Battery Status and Virtual Sensors
    batteryStatusVirtualSensors: BatteryStatusVirtualSensors

    # Locations of data in advertising packet
    __PRODUCT_TYPE_RANGE = slice(2, 3)
    __SERIAL_RANGE = slice(3, 7)
    __TEMPERATURE_RANGE = slice(7, 20)
    __MODE_COLOR_ID_RANGE = slice(20, 21)
    __DEVICE_STATUS_RANGE = slice(21, 22)

    def __init__(self, data: bytearray):
        if len(data) < AdvertisingData.__TEMPERATURE_RANGE.stop:
            return None

        '''
        self.min_sequence_number = data[ProbeStatus.__MIN_SEQ_RANGE]

        self.max_sequence_number = data[ProbeStatus.__MAX_SEQ_RANGE]

        # Temperatures (8 13-bit) values
        temp_data = data[ProbeStatus.__TEMPERATURE_RANGE]
        self.temperatures = ProbeTemperatures.from_raw_data(bytes=temp_data)

        # Decode ModeId byte if present
        if len(data) >= ProbeStatus.__MODE_COLOR_ID_RANGE.stop:
            byte = data[ProbeStatus.__MODE_COLOR_ID_RANGE][0]
            self.mode_id = ModeId.from_byte(byte)
        else:
            self.mode_id = ModeId.default_values()

        if len(data) >= ProbeStatus.__DEVICE_STATUS_RANGE.stop:
            byte = data[ProbeStatus.__DEVICE_STATUS_RANGE][0]
            self.battery_status_virtual_sensors = BatteryStatusVirtualSensors.from_byte(
                byte)
        else:
            self.battery_status_virtual_sensors = BatteryStatusVirtualSensors.default_values()

        if len(data) >= ProbeStatus.__PREDICTION_STATUS_RANGE.stop:
            bytes = data[ProbeStatus.__PREDICTION_STATUS_RANGE]
            self.prediction_status = PredictionStatus.from_bytes(bytes)
        else:
            self.prediction_status = None'''

        # Product type (1 byte)
        raw_type = data[AdvertisingData.__PRODUCT_TYPE_RANGE]
        self.type = CombustionProductType(
            raw_type[0]) or CombustionProductType.unknown

        # Device Serial number (4 bytes)
        # Reverse the byte order (this is a little-endian packed bitfield)
        raw_serial = data[AdvertisingData.__SERIAL_RANGE]
        raw_serial.reverse()
        value: int = 0
        for byte in raw_serial:
            value = value << 8
            value = value | int(byte)

        self.serial_number = value

        # Temperatures (8 13-bit) values
        temp_data = data[AdvertisingData.__TEMPERATURE_RANGE]
        self.temperatures = ProbeTemperatures.from_raw_data(bytes=temp_data)

        # Decode ModeId byte if present
        if len(data) >= AdvertisingData.__MODE_COLOR_ID_RANGE.stop:
            byte = data[AdvertisingData.__MODE_COLOR_ID_RANGE][0]
            self.mode_id = ModeId.from_byte(byte)
        else:
            self.mode_id = ModeId.default_values()

        if len(data) >= AdvertisingData.__DEVICE_STATUS_RANGE.stop:
            byte = data[AdvertisingData.__DEVICE_STATUS_RANGE][0]
            self.battery_status_virtual_sensors = BatteryStatusVirtualSensors.from_byte(
                byte)
        else:
            self.battery_status_virtual_sensors = BatteryStatusVirtualSensors.default_values()
