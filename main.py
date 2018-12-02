# import time
# from subprocess import call
# from vibratesw import vibrateSW
# from Button_Interface import Button
# from requset_server import RequestMgr
# from Battery_Indicator import Battery
from unicornled import UnicornLED
from bluetoothrfcomm import BluetoothRFCOMM
from filemgr import FileManager
from gyroscope import Mpu


def main():
    # sw = vibrateSW(23)
    # battery_level = Battery()
    # requestMgr = RequestMgr()
    # start = Button()
    file_manager = FileManager()
    bluetooth = BluetoothRFCOMM()
    mpu = Mpu()
    led = UnicornLED(file_manager.read_state(), file_manager.save_state)
    try:
        # sw.run(led.setEmergency, bluetooth.sendMsg)
        # Battery.run(bluetooth.sendMsg())
        # requestMgr.run(gyroSensor.gyroData)
        # start.run()
        led.run()
        bluetooth.run(led.set_attribute,
                      led.get_led_info,
                      mpu.set_bluetooth_trigger,
                      file_manager.save_image_LED,
                      file_manager.get_exists_LED)
        mpu.run(bluetooth.send_message)

    except KeyboardInterrupt:
        print("main KeyboardInterrupt")

    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("main KeyboardInterrupt")


if __name__ == '__main__':
    main()
