import time
import threading
import subprocess
import RPi.GPIO as GPIO
from pattern_manager import PatternMgr

# ----------------DEFINE BUTTON ATTRIBUTE---------------- #
PIN_NUM = 16
LONG_TIME = 2500
SHORT_TIME = 1000
SEC_TO_MS = 1000
# -------------------------------------------------------- #

class Button(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_NUM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.onOffTrigger = False

    def time_cal(self, pressed_time):
        a = GPIO.wait_for_edge(PIN_NUM, GPIO.FALLING, timeout=LONG_TIME)
        print("time cal")

        if PIN_NUM is a:
            activated_Time = time.time() - pressed_time
        else:
            return LONG_TIME / SEC_TO_MS
        return activated_Time

    def push(self):
        while True:
            i = GPIO.wait_for_edge(PIN_NUM, GPIO.RISING)

            if i == PIN_NUM:
                falling_time = self.time_cal(time.time())
                if falling_time == LONG_TIME / SEC_TO_MS:
                    print("bluetooth  on")
                    subprocess.call(['sudo', 'bluetoothctl', 'discoverable', 'yes'])

                elif falling_time < SHORT_TIME / SEC_TO_MS:
                    if self.onOffTrigger is True:
                        self.onOffTrigger = False
                    else:
                        self.onOffTrigger = True
                    PatternMgr.set_break_trigger(True)
                    print("power on & off")

    def get_onoff(self):
        return self.onOffTrigger

    def run(self):
        t1 = threading.Thread(target=self.push)
        t1.daemon = True
        t1.start()
