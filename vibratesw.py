import RPi.GPIO as GPIO
import time
import threading


class vibrateSW(object):

    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback, bouncetime=1)
        self.count = 0

    def callback(self):
        self.count += 1

    def vibrate_sensor(self, ledcallback, bluetoothcallback):
        try:
            while True:
                time.sleep(1)

                if self.count >= 10:
                    print("Detect vibrate " + self.count)
                    ledcallback()
                    bluetoothcallback("Detect vibrate")

                else:
                    print("Not detect vibrate")

                # time.sleep(5)
                self.count = 0

            # while True:
            #     result = GPIO.input(23)
            #     if result == 1:
            #         print("detect vibrate.")
            #         time.sleep(0.05)
            #
            #     else:
            #         print("not detect vibrate.")
            #         time.sleep(0.05)

        except KeyboardInterrupt:
            GPIO.cleanup()

    def run(self, ledcb, bluetoothcb):
        t1 = threading.Thread(target=self.vibrate_sensor, args=(ledcb, bluetoothcb, ))
        t1.daemon = True
        t1.start()

# END

