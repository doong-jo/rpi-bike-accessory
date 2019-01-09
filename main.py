from bluetoothrfcomm import BluetoothRFCOMM
from neopixel_strip import NeopixelStrip

import subprocess
import RPi.GPIO as GPIO

def main():
    # turn on bluetooth discoverable
    subprocess.call(['sudo', 'bluetoothctl', 'discoverable', 'yes'])

    led = NeopixelStrip(12, 5, 0)
    bluetoothRFCOMM = BluetoothRFCOMM()

    led.run()
    bluetoothRFCOMM.run(led.set_attribute)

    # requestMgr.run(gyroSensor.gyroData)

    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("main KeyboardInterrupt")


if __name__ == '__main__':
    main()
    GPIO.cleanup(0)
    subprocess.call(['sudo', 'bluetoothctl', 'discoverable', 'no'])