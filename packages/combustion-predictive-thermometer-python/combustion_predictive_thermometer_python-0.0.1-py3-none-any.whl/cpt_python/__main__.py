from cptpython.bluetooth_data import probe_status
from cptpython import blemanager

import asyncio
from bleak import BleakScanner, BleakClient, BleakError, BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import logging

if __name__ == '__main__':
    manager = blemanager.BleManager()
    asyncio.run(manager.start_scanning())

'''logger = logging.getLogger(__name__)

known_devices = []


def match_known_address(device: BLEDevice, adv_data: AdvertisementData):
    return "00000100-CAAB-3792-3D44-97AE51C1407A" in [s.upper() for s in adv_data.service_uuids] and device.address not in known_devices


def disconnected(client: BleakClient):
    print("disconnected!")


def callback(sender: BleakGATTCharacteristic, data: bytearray):
    status = probe_status.ProbeStatus(data)
    print(status.temperatures.values)
    print(f"Probe is in {status.mode_id.mode}")


async def main():
    while True:
        print("scanning!")
        device = await BleakScanner.find_device_by_filter(match_known_address)
        if device is None:
            await asyncio.sleep(3)
            continue

        client = BleakClient(device, disconnected_callback=disconnected)
        try:
            await client.connect()
            known_devices.append(device.address)
            print("conencted!")
            await client.start_notify("00000101-CAAB-3792-3D44-97AE51C1407A", callback=callback)
            print("started notift")
        except BleakError as e:
            print("Error!")
            print(e)
            # if failed to connect, this is a no-op, if failed to start notifications, it will disconnect
            await client.disconnect()


if __name__ == '__main__':
    log_level = logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main())
    raw_message = bytearray(
        b'\x00\x00\x00\x00o\x01\x00\x004#g\xf0\x8c\x9f\xe14\xa2\xc6\xd7H\x1b\x00\xc0\x02\x00\x00\xf0\xff_3')
    print(raw_message.hex())

    x = probe_status.ProbeStatus(raw_message)
    print(x.temperatures.values)'''
