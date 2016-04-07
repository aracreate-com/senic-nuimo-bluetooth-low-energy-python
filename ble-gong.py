import time
import uuid
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

ble = Adafruit_BluefruitLE.get_provider()
UART_SERVICE = uuid.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')


def main():
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using : {0}'.format(adapter.name))
    ble.disconnect_devices([UART_SERVICE])
    adapter.start_scan()
    time.sleep(5)

    devices = ble.find_devices(service_uuids=[UART_SERVICE])
    time.sleep(5)

    gong = None
    for device in devices:
        print('Found device: {0}, id: {1}'.format(device.name, device.id))
        if device.name == 'BLEGong':
            print 'Found gong', device.id,
            gong = device
            adapter.stop_scan()
            break

    gong.connect()
    print ('Gong Connected')

    UART.discover(gong)
    print 'Gong Discovered'

    gong_uart = UART(gong)

    adapter.power_off()
    print 'Disconnected'


ble.initialize()
ble.run_mainloop_with(main)
