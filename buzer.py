import RPi.GPIO as GPIO
import threading
import time

GPIO_PIN = 18  # PWM pin num 22
EFFECT_SOUND_INTERVAL = 1

BUZER_FREQUENCY = 2000
BUZER_START_AMOUNT = 100

class Buzer(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.OUT)
        self._buzer = GPIO.PWM(GPIO_PIN, BUZER_FREQUENCY)
        self._enable = False
        self._stTime = 0
        pass

    def start_sound(self, enable):
        self._enable = enable
        self._stTime = time.time()
        self._buzer.start(BUZER_START_AMOUNT)

    def effect_sound(self):
        while True:
            # self._buzer.start(0)
            if self._enable:
                if time.time() - self._stTime < EFFECT_SOUND_INTERVAL:
                    # print "running buzer"
                    pass
                else:
                    self._enable = False
                    self._buzer.start(0)

    def run(self):
        t1 = threading.Thread(target=self.effect_sound)
        t1.daemon = True
        t1.start()