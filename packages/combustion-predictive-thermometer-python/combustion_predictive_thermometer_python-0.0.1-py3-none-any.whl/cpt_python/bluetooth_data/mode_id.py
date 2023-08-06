from enum import Enum


class ProbeID(Enum):
    ID1 = 0x00
    ID2 = 0x01
    ID3 = 0x02
    ID4 = 0x03
    ID5 = 0x04
    ID6 = 0x05
    ID7 = 0x06
    ID8 = 0x07


class ProbeColor(Enum):
    color1 = 0x00
    color2 = 0x01
    color3 = 0x02
    color4 = 0x03
    color5 = 0x04
    color6 = 0x05
    color7 = 0x06
    color8 = 0x07


class ProbeMode(Enum):
    normal = 0x00
    instantRead = 0x01
    reserved = 0x02
    error = 0x03


class ModeId:
    id: ProbeID
    color: ProbeColor
    mode: ProbeMode

    __PRODE_ID_MASK: int = 0x7
    __PRODE_ID_SHIFT: int = 5
    __PRODE_COLOR_MASK: int = 0x7
    __PRODE_COLOR_SHIFT: int = 2
    __PRODE_MODE_MASK: int = 0x3

    def __init__(self, id: ProbeID, color: ProbeColor, mode: ProbeMode):
        self.id = id
        self.color = color
        self.mode = mode

    @staticmethod
    def from_byte(byte: int) -> "ModeId":
        raw_prob_id = (
            byte >> ModeId.__PRODE_ID_SHIFT) & ModeId.__PRODE_ID_MASK
        id = ProbeID(raw_prob_id) or ProbeID.ID1

        raw_probe_color = (
            byte >> ModeId.__PRODE_COLOR_SHIFT) & ModeId.__PRODE_COLOR_MASK
        color = ProbeColor(raw_probe_color) or ProbeColor.color1

        raw_mode = byte & (ModeId.__PRODE_MODE_MASK)
        mode = ProbeMode(raw_mode) or ProbeMode.normal

        return ModeId(id=id, color=color, mode=mode)

    @staticmethod
    def default_values() -> "ModeId":
        return ModeId(id=ProbeID.ID1, color=ProbeColor.color1, mode=ProbeMode.normal)
