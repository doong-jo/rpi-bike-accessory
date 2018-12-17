from unicornled import UnicornLED
from bluetoothrfcomm import BluetoothRFCOMM
from gyroscope import Mpu
from buzer import Buzer
from toggle_button import Button
from battery import Battery
# from requset_server import RequestMgr

import RPi.GPIO as GPIO

def main():
    battery = Battery()
    bluetoothButton = Button()
    led = UnicornLED()
    bluetoothRFCOMM = BluetoothRFCOMM()
    mpu = Mpu()
    buzer = Buzer()

    # requestMgr = RequestMgr()

    battery.run()
    bluetoothButton.run()
    led.run()
    bluetoothRFCOMM.run(led.set_attribute, led.get_led_info, mpu.set_bluetooth_trigger)
    mpu.run()
    buzer.run()

    # requestMgr.run(gyroSensor.gyroData)

    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("main KeyboardInterrupt")



if __name__ == '__main__':
    main()
    GPIO.cleanup(0)
