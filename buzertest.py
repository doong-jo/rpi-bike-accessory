import RPi.GPIO as GPIO
import time

pin = 18  # PWM pin num 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(18, 5000)
p.start(100)
try:
    while True:
        print ''

except KeyboardInterrupt:
    GPIO.cleanup()