import threading
from neopixel import *
import argparse
import time
import datetime
from pytz import timezone


LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 30     # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_STRIP      = ws.WS2811_STRIP_GRB
LED_TURN_ON     = Color(255, 0, 0)
LED_TURN_OFF    = Color(0, 0, 0)

LED_PASS_ATTRIBUTE = -1

class NeopixelStrip(object):
    def __init__(self, pin, pixels, channel):
        self._strip = Adafruit_NeoPixel(pixels, pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                                       channel, LED_STRIP)
        self._strip.begin()
        self.PIXELS = pixels
        self._brightness = 255
        self._color = Color(self._brightness, 0, 0)

        self._curImageName = 0
        self._curSpeed = 0.5
        self._curType = -1
        self._syncTrigger = False
        self._syncSec = 0

    def set_attribute(self, imagename, type, speed, brightness, sync):
        # set attributes from bluetooth data

        # if self._IsInturrpt is True:
        #     return

        if imagename != LED_PASS_ATTRIBUTE:
            self._curImageName = imagename

        if type != LED_PASS_ATTRIBUTE:
            self._curType = type

        if speed != LED_PASS_ATTRIBUTE:
            self._curSpeed = speed

        if brightness != LED_PASS_ATTRIBUTE:
            self._brightness = brightness

        if sync != LED_PASS_ATTRIBUTE:
            self._syncTrigger = True
            self._syncSec = sync

        obj_LED = {}
        obj_LED['LED_STATE'] = []
        obj_LED['LED_STATE'].append({
            'index': self._curImageName,
            'type': self._curType,
            'speed': self._curSpeed,
            'brightness': self._brightness
        })

    def basePattern(self):
        for idx in range(0, self.PIXELS):
            if self.run_break() is True:
                return
            self._strip.setPixelColor(idx, LED_TURN_ON)

        self._strip.show()

    def runPattern(self):
        for idx in range(0, self.PIXELS):
            self._strip.setPixelColor(idx, LED_TURN_ON)

        self._strip.show()
        time.sleep(1)

        for idx in range(0, self.PIXELS):
            self._strip.setPixelColor(idx, LED_TURN_OFF)

        self._strip.show()
        time.sleep(1)

    def show(self):
        while True:
            if self._syncTrigger is True:
                curDate = datetime.datetime.now(timezone('Asia/Seoul'))
                if int(curDate.second) == int(self._syncSec):
                    self._syncTrigger = False

                print curDate.second
                print self._syncSec

            if self._curImageName == "start" and self._syncTrigger is False:
                self.runPattern()
            else:
                self.basePattern()

    def clear(self):
        for idx in range(0, self.PIXELS):
            self._strip.setPixelColor(idx, LED_TURN_OFF)

    def run_break(self):
        if self._curImageName != 0:
            self.clear()
            return True
        else:
            return False

    def run(self):
        self.thread = threading.Thread(target=self.show, args=())
        self.thread.daemon = True
        self.thread.start()

