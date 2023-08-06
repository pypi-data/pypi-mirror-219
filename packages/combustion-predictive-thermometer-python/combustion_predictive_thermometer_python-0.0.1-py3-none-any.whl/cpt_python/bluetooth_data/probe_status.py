from cpt_python.bluetooth_data.probe_temperatures import ProbeTemperatures
from cpt_python.bluetooth_data.mode_id import ModeId
from cpt_python.bluetooth_data.battery_status_virtual_sensors import BatteryStatusVirtualSensors
from cpt_python.bluetooth_data.prediction_status import PredictionStatus
# Message containing Probe status information.


class ProbeStatus:
    # Minimum sequence number of records in Probe's memory.
    min_sequence_number: int
    # Maximum sequence number of records in Probe's memory.
    max_sequence_number: int
    # Current temperatures sent by Probe.
    temperatures: ProbeTemperatures
    # ModeId (Probe color, ID, and mode)
    mode_id: ModeId
    # Battery Status and Virtual Sensors
    battery_status_virtual_sensors: BatteryStatusVirtualSensors
    # Prediction Status
    prediction_status: PredictionStatus

    # Locations of data in status packet
    __MIN_SEQ_RANGE = slice(0, 4)
    __MAX_SEQ_RANGE = slice(4, 8)
    __TEMPERATURE_RANGE = slice(8, 21)
    __MODE_COLOR_ID_RANGE = slice(21, 22)
    __DEVICE_STATUS_RANGE = slice(22, 23)
    __PREDICTION_STATUS_RANGE = slice(23, 30)

    def __init__(self, data: bytearray):
        if len(data) < ProbeStatus.__TEMPERATURE_RANGE.stop:
            return None

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
            self.prediction_status = None

    def __str__(self) -> str:
        temps = ", ".join([f"{temp:.1f}"
                          for temp in self.temperatures.values])
        string = f"Probe status. Mode: {self.mode_id.mode.name}. Temps: {temps}"
        return string
