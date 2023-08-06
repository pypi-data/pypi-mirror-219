from enum import Enum


class PredictionState(Enum):
    probeNotInserted = 0x00
    probeInserted = 0x01
    cooking = 0x02
    predicting = 0x03
    removalPredictionDone = 0x04
    unknown = 0x0F


class PredictionMode(Enum):
    none = 0x00
    timeToRemoval = 0x01
    removalAndResting = 0x02
    reserved = 0x03


class PredictionType(Enum):
    none = 0x00
    removal = 0x01
    resting = 0x02
    reserved = 0x03


class PredictionStatus:
    prediction_state: PredictionState
    prediction_mode: PredictionMode
    prediction_type: PredictionType
    prediction_set_point_temperature: float
    heat_start_temperature: float
    prediction_value_seconds: int
    estimated_core_temperature: float

    __PREDICTION_STATE_MASK = 0xF
    __PREDICTION_MODE_MASK = 0x3
    __PREDICTION_TYPE_MASK = 0x3

    def __init__(
        self,
        prediction_state: PredictionState,
        prediction_mode: PredictionMode,
        prediction_type: PredictionType,
        prediction_set_point_temperature: float,
        heat_start_temperature: float,
        prediction_value_seconds: int,
        estimated_core_temperature: float,
    ):
        self.prediction_state = prediction_state
        self.prediction_mode = prediction_mode
        self.prediction_type = prediction_type
        self.prediction_set_point_temperature = prediction_set_point_temperature
        self.heat_start_temperature = heat_start_temperature
        self.prediction_value_seconds = prediction_value_seconds
        self.estimated_core_temperature = estimated_core_temperature

    @staticmethod
    def from_bytes(bytes: list[int]) -> "PredictionStatus":
        raw_prediction_state = bytes[0] & PredictionStatus.__PREDICTION_STATE_MASK
        prediction_state = PredictionState(
            raw_prediction_state) or PredictionState.unknown

        raw_prediction_mode = (
            bytes[0] >> 4) & PredictionStatus.__PREDICTION_MODE_MASK
        prediction_mode = PredictionMode(
            raw_prediction_mode) or PredictionMode.none

        raw_prediction_type = (
            bytes[0] >> 6) & PredictionStatus.__PREDICTION_TYPE_MASK
        prediction_type = PredictionType(
            raw_prediction_type) or PredictionType.none

        # 10 bit field
        raw_set_point = (bytes[2] & 0x03) << 8 | (bytes[1])
        set_point = float(raw_set_point) * 0.1

        # 10 bit field
        raw_heat_start = (bytes[3] & 0x0F) << 6 | (bytes[2] & 0xFC) >> 2
        heat_start = float(raw_heat_start) * 0.1

        # 17 bit field
        seconds = (bytes[5] & 0x1F) << 12 | (
            bytes[4]) << 4 | (bytes[3] & 0xF0) >> 4

        # 11 bit field
        raw_core = (bytes[6]) << 3 | (bytes[5] & 0xE0) >> 5
        estimated_core = (float(raw_core) * 0.1) - 20.0

        return PredictionStatus(prediction_state=prediction_state,
                                prediction_mode=prediction_mode,
                                prediction_type=prediction_type,
                                prediction_set_point_temperature=set_point,
                                heat_start_temperature=heat_start,
                                prediction_value_seconds=seconds,
                                estimated_core_temperature=estimated_core)
