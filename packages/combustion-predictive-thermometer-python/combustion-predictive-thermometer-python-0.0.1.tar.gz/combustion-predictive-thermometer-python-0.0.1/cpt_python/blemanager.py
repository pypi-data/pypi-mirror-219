import asyncio
from bleak import BleakScanner, BleakClient, BleakError, BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from typing import Optional, List
from cpt_python.bluetooth_data import probe_status


class BleManager:
    scanner: BleakScanner

    __NEEDLE_SERVICE = "00000100-CAAB-3792-3D44-97AE51C1407A"
    __DEVICE_STATUS_CHARACTERSTIC = "00000101-CAAB-3792-3D44-97AE51C1407A"
    known_devices: List[str] = []

    def match_needle(self, device: BLEDevice, adv_data: AdvertisementData):
        return self.__NEEDLE_SERVICE in [s.upper() for s in adv_data.service_uuids] and device.address not in self.known_devices

    def disconnected(self, client: BleakClient):
        print("disconnected!")

    async def start_scanning(self, scanner: Optional[BleakScanner] = None):
        self.scanner = scanner if scanner is not None else BleakScanner()
        while True:
            print("Started scanning!")
            device = await self.scanner.find_device_by_filter(self.match_needle)
            if device is None:
                await asyncio.sleep(3)
                continue
            await self.subscribe_to_notifications(device)

    async def subscribe_to_notifications(self, device: BleakClient):
        client = BleakClient(
            device, disconnected_callback=self.disconnected)
        await client.connect()
        self.known_devices.append(client.address)
        await client.start_notify(self.__DEVICE_STATUS_CHARACTERSTIC, callback=self.callback)

    def callback(self, sender: BleakGATTCharacteristic, data: bytearray):
        status = probe_status.ProbeStatus(data)
        print(status)

    '''

    def disconnected(client: BleakClient):
        print("disconnected!")

    

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
                await client.disconnect()'''

    '''async def simple_callback(device: BLEDevice, advertisement_data: AdvertisementData):
        # print(advertisement_data.service_data)
        print(device.address)
        with BleakClient(device.address) as client:
            print("hello")
            model_number = await client.read_gatt_char("00000100-CAAB-3792-3D44-97AE51C1407A")
            print("Model Number: {0}".format("".join(map(chr, model_number))))
        # logger.info("%s: %r", device.address, advertisement_data)


    async def main():
        scanner = BleakScanner(
            simple_callback, ["00000100-CAAB-3792-3D44-97AE51C1407A"]
        )

        while True:
            logger.info("(re)starting scanner")
            await scanner.start()
            await asyncio.sleep(5.0)
            await scanner.stop()

    '''
    '''if __name__ == "__main__":

        log_level = logging.INFO
        logging.basicConfig(
            level=log_level,
            format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
        )

        asyncio.run(main())'''
