import RPi.GPIO as GPIO
import threading
import time

GPIO_PIN = 18  # PWM pin num 22
EFFECT_SOUND_INTERVAL = 2

BUZER_FREQUENCY = 1000
BUZER_START_AMOUNT = 100

class Buzer(object):
    def __init__(self):
        pass

    buzer = None
    enable = False
    stTime = 0

    @staticmethod
    def start_sound(enable):
        if Buzer.buzer is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_PIN, GPIO.OUT)
            Buzer.buzer = GPIO.PWM(GPIO_PIN, BUZER_FREQUENCY)

        if Buzer.enable is False:
            Buzer.enable = enable
            Buzer.stTime = time.time()
            Buzer.buzer.start(BUZER_START_AMOUNT)
            print "running buzer"

    def effect_sound(self):
        while True:
            if Buzer.enable:
                if time.time() - Buzer.stTime < EFFECT_SOUND_INTERVAL:
                    pass
                else:
                    Buzer.enable = False
                    Buzer.buzer.start(0)
                    print "stop buzer"

    def run(self):
        t1 = threading.Thread(target=self.effect_sound)
        t1.daemon = True
        t1.start()
