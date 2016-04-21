import time
import uuid

import Adafruit_BluefruitLE

SERVICE_UUIDS = [
    uuid.UUID('0000180f-0000-1000-8000-00805f9b34fb'),  # Battery
    uuid.UUID('f29b1525-cb19-40f3-be5c-7241ecb82fd2'),  # Sensors
    uuid.UUID('f29b1523-cb19-40f3-be5c-7241ecb82fd1')  # LED
]

CHARACTERISTIC_UUIDS = {
    uuid.UUID('00002a19-0000-1000-8000-00805f9b34fb'),  # BATTERY
    uuid.UUID('f29b1529-cb19-40f3-be5c-7241ecb82fd2'),  # BUTTON
    uuid.UUID('f29b1528-cb19-40f3-be5c-7241ecb82fd2'),  # ROTATION
    uuid.UUID('f29b1527-cb19-40f3-be5c-7241ecb82fd2'),  # SWIPE
    uuid.UUID('f29b1526-cb19-40f3-be5c-7241ecb82fd2'),  # FLY
    uuid.UUID('f29b1524-cb19-40f3-be5c-7241ecb82fd1')  # LED_MATRIX
}

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


def main():
    # Clear previously received data from the controller/adapter
    ble.clear_cached_data()

    # Connect to the default or first adapter and start scan
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using : {0}'.format(adapter.name))
    ble.disconnect_devices(SERVICE_UUIDS)
    adapter.start_scan()

    # It needs bit of time to scan the devices.
    # Some Peripherals advertise in different
    time.sleep(5)

    devices = ble.find_devices(service_uuids=[SERVICE_UUIDS[2]])

    for device in devices:
        print('Found device: {0}, id: {1}'.format(device.name, device.id))

        if device.name == 'NuimoARA':
            print 'Found NuimoARA'
            nuimo = device

            # Once NuimoARA is found, then stop scanning
            adapter.stop_scan()

            nuimo.connect()
            print 'Connected to NuimoARA'

            nuimo.discover(SERVICE_UUIDS, CHARACTERISTIC_UUIDS)
            print 'Discovery Mode'

            led_matrix_service = nuimo.find_service(SERVICE_UUIDS[2])
            print('Led Matrix Service : {0}'.format(led_matrix_service.uuid))
            led_matrix_characteristic = led_matrix_service.list_characteristics()[0]
            print('Led Matrix Characteristic : {0}'.format(led_matrix_characteristic.uuid))

            led_matrix_characteristic.write_value('FFFFFFFFFFFFF')
            print 'Wrote to LED'

            print 'UUIDs of Sensor Characteristics'
            sensor_service = nuimo.find_service(SERVICE_UUIDS[1])
            sensor_characteristics = sensor_service.list_characteristics()
            for sensor_characteristic in sensor_characteristics:
                print sensor_characteristic.uuid

            button_characteristic = sensor_characteristics[0]
            print('Button Characteristic : {0}'.format(button_characteristic.uuid))

            swipe_characteristic = sensor_characteristics[2]
            print('Swipe Characteristic : {0}'.format(swipe_characteristic.uuid))

            def button_received(data):
                print 'Button: ', map(ord, data)

            def swipe_received(data):
                print 'Swipe: ', map(ord, data)

            button_characteristic.start_notify(button_received)
            swipe_characteristic.start_notify(swipe_received)

            while True:
                time.sleep(1)

    adapter.power_off()
    print 'Disconnected from NuimoARA'


ble.initialize()
ble.run_mainloop_with(main)
