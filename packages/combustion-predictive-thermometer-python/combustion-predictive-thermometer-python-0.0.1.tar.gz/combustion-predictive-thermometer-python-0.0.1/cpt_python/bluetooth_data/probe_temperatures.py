class ProbeTemperatures:
    values: list[float]

    def __init__(self, values: list[float]):
        self.values = values

    @staticmethod
    def from_raw_data(bytes: list[int]) -> "ProbeTemperatures":
        # Reverse the byte order (this is a little-endian packed bitfield)
        bytes.reverse()
        raw_temps: list[int] = []
        # Add the temperatures in reverse order (reversed as it's a little-endian packed bitfield)
        raw_temps.insert(0, (bytes[0] & 0xFF) << 5 | (bytes[1] & 0xF8) >> 3)
        raw_temps.insert(0, (bytes[1] & 0x07) << 10 | (
            bytes[2] & 0xFF) << 2 | (bytes[3] & 0xC0) >> 6)
        raw_temps.insert(0, (bytes[3] & 0x3F) << 7 | (bytes[4] & 0xFE) >> 1)
        raw_temps.insert(0, (bytes[4] & 0x01) << 12 | (
            bytes[5] & 0xFF) << 4 | (bytes[6] & 0xF0) >> 4)
        raw_temps.insert(0, (bytes[6] & 0x0F) << 9 | (
            bytes[7] & 0xFF) << 1 | (bytes[8] & 0x80) >> 7)
        raw_temps.insert(0, (bytes[8] & 0x7F) << 6 | (bytes[9] & 0xFC) >> 2)
        raw_temps.insert(0, (bytes[9] & 0x03) << 11 | (
            bytes[10] & 0xFF) << 3 | (bytes[11] & 0xE0) >> 5)
        raw_temps.insert(0, (bytes[11] & 0x1F) << 8 | (bytes[12] & 0xFF) >> 0)

        temperatures = [temp * .05 - 20.0 for temp in raw_temps]
        return ProbeTemperatures(values=temperatures)
