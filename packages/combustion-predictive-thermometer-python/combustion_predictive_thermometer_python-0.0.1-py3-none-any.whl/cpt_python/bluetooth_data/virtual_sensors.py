from enum import Enum


class VirtualCoreSensor(Enum):
    T1 = 0x00
    T2 = 0x01
    T3 = 0x02
    T4 = 0x03
    T5 = 0x04
    T6 = 0x05


class VirtualSurfaceSensor(Enum):
    T4 = 0x00
    T5 = 0x01
    T6 = 0x02
    T7 = 0x03


class VirtualAmbientSensor(Enum):
    T5 = 0x00
    T6 = 0x01
    T7 = 0x02
    T8 = 0x03


class VirtualSensors:
    virtual_core: VirtualCoreSensor
    virtual_surface: VirtualSurfaceSensor
    virtual_ambient: VirtualAmbientSensor

    __VIRTUAL_SURFACE_SHIFT: int = 3
    __VIRTUAL_AMBIENT_SHIFT: int = 5

    __VIRTUAL_CORE_MASK = 0x7
    __VIRTUAL_AMBIENT_MASK = 0x3
    __VIRTUAL_SURFACE_MASK = 0x3

    def __init__(self, virtual_core: VirtualCoreSensor, virtual_surface: VirtualSurfaceSensor, virtual_ambient: VirtualAmbientSensor):
        self.virtual_core = virtual_core
        self.virtual_surface = virtual_surface
        self.virtual_ambient = virtual_ambient

    @staticmethod
    def from_byte(byte: int) -> "VirtualSensors":
        raw_virtual_core = (byte) & VirtualSensors.__VIRTUAL_CORE_MASK
        virtual_core = VirtualCoreSensor(
            raw_virtual_core) or VirtualCoreSensor.T1

        raw_virtual_surface = (
            byte >> VirtualSensors.__VIRTUAL_SURFACE_SHIFT) & VirtualSensors.__VIRTUAL_SURFACE_MASK
        virtual_surface = VirtualSurfaceSensor(
            raw_virtual_surface) or VirtualSurfaceSensor.T4

        raw_virtual_ambient = (
            byte >> VirtualSensors.__VIRTUAL_AMBIENT_SHIFT) & VirtualSensors.__VIRTUAL_AMBIENT_MASK
        virtual_ambient = VirtualAmbientSensor(
            raw_virtual_ambient) or VirtualAmbientSensor.T5

        return VirtualSensors(virtual_core=virtual_core, virtual_surface=virtual_surface, virtual_ambient=virtual_ambient)
