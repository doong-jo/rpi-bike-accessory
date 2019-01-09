from unicornled import UnicornLED
from bluetoothrfcomm import BluetoothRFCOMM
from gyroscope import Mpu
from toggle_button import Button

# from requset_server import RequestMgr

import subprocess
import RPi.GPIO as GPIO

def main():
    # turn on bluetooth discoverable
    subprocess.call(['sudo', 'bluetoothctl', 'discoverable', 'yes'])

    bluetoothButton = Button()
    led = UnicornLED()
    bluetoothRFCOMM = BluetoothRFCOMM()
    mpu = Mpu()

    # requestMgr = RequestMgr()

    bluetoothButton.run()
    led.run()
    bluetoothRFCOMM.run(led.set_attribute, led.get_led_info, mpu.set_bluetooth_trigger)
    mpu.run()

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
