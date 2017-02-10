# Nuimo Client on MacOS and Linux
These python scripts are used for prototyping with [Nuimo](https://www.senic.com) which implement Nuimo's GATT Profile using Adafruit BLE library for Corebluetooth and Bluez. There these scripts can be used on MacOS and Linux.

## GATT Profile [ [PDF](https://files.senic.com/nuimo-gatt-profile.pdf) ]
Nuimo Application defines its own GATT (Generic Attribute) Profile along with standard services such as Device Information Service (DIS) and Battery Service (BAS). When Nuimo is connected to a BLE Central, Nuimo App on BLE Central discovers all the services and characteristics and assigns Handle IDs which are used internally to refer the characteristics. Services and characteristics are discovered in the order of their initialization on the firmware side. 

For example Gesture characteristic is initialized first and button initialized second, then Handle ID of gesture char will 0x01 and button char will be 0x02 on the BLE Central device. These Handle IDs are cached on the BLE Central side and caches are cleared only when Bluetooth is switched OFF/ON. This causes issue when new Service or Characteristic is added to GATT profile or the order of initialization is changed on firmware.

- **Device Information Service**
	- UUID Base : 0000xxxx-0000-1000-8000-00805F9B34FB
	- Service UUID : 0x180A
	- Characteristics
		- Manufacturer Name Characteristic
			- UUID: 0x2A29
			- String (variable length) = Senic
		- Model Number Characteristic 
			- UUID: 0x2A24
			- String (variable length) = Color of Nuimo (Black, White, Gold)
		- Hardware Revision Characteristic
			- UUID: 0x2A27
			- String (variable length) = 1.4
		- Firmware Revision Characteristic
			- UUID: 0x2A26
			- String (variable length) = 2.4.1

- **Battery Service**
	- UUID Base : 0000xxxx-0000-1000-8000-00805F9B34FB
	- Service UUID : 0x180F
	- Characteristics
		- Battery Level Characteristic
			- UUID : 0x2A19
			- Read / Notify 
			- Notifies battery level in percentage which is calculated by doing ADC on battery voltage
			- 1 byte unsigned integer, 0 to 100 = Battery percentage

- **Nuimo Service**
	- UUID Base: F29Bxxxx-CB19-40F3-BE5C-7241ECB82FD2
	- Service UUID : 0x1525
	- Characteristics
		- Gesture Characteristic
			- UUID : 0x1526
			- Read / Notify
			- Notifies detected fly gestures and proximity gestures
			- 2 bytes unsigned integer
			- 1st byte : 0 = Fly Left, 1 = Fly Right, 4 = Proximity distance (if this, proximity distance should be calculated from 2nd byte otherwise ignored)
			- 2nd byte : 0 to 255=Proximity distance
			
		- Touch Characteristic
			- UUID : 0x1527
			- Read / Notify
			- Notifies detected swipe, touch and long touch events
			- 1 byte unsigned integer :  0 = Swipe Left, 1 = Swipe Right, 2 = Swipe Up, 3 = Swipe Down, 4 = Touch Left, 5 = Touch Right, 6 = Touch Top, 7 = Touch Bottom, 8 = LongTouch Left, 9 = LongTouch Right, 10 = LongTouch Top, 11 = LongTouch Bottom
		
		- Encoder Characteristic
			- UUID : 0x1528
			- Read / Notify
			- Notifies direction and relative rotational distance from last position of encoder
			- 2 bytes signed integer : >0 = Clockwise Rotation, <0 = Counter Clockwise Rotation
		
		- Button Characteristic
			- UUID : 0x1529
			- Read / Notify
			- Notifies press and release events of button
			- 1 byte unsigned integer : 0 = Release, 1 = Press

		- Gesture Calibration Characteristic
			- UUID : 0x152C
			- 1 byte Write
			- Writing 0x01 will do calibration of gesture sensor on Nuimo

		- LED Characteristic
			- UUID : 0x152D
			- Read / Write / Write-Without-Response
			- Writes byte-array to control 9x9 LED Matrix
			- 13 bytes unsigned integer
			- 1 to 11 bytes represents LED Matrix
			- 11th byte (LSB -> MSB)
				- Bit 1: represents 81st LED
				- Bit 2: reserved
				- Bit 3: reserved
				- Bit 4: reserved
				- Bit 5: 0 = Disable Onion Skinning Effect, 1 = Enable Onion Skinning Effect (Visual effect which allows every consequent frame/LED Matrix to fade in with previous frame; than abruptly clearing previous frame to show the new frame)
				- Bit 6: 1 = Play inbuilt animation (Use 1st byte of LED Matrix to denote which animation to be played)
				- Bit 7: reserved
				- Bit 8: reserved
			- 12th byte 0 to 255 = LED Brightness
			- 23th byte 0 to 255 = LED Display duration in 0 to 25.5 seconds
