import threading
from neopixel import *
from pattern_manager import PatternMgr
import time
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 30     # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_STRIP       = ws.WS2811_STRIP_GRB

LED_TURN_ON     = Color(255, 0, 0)
LED_TURN_OFF    = Color(0, 0, 0)

class NeopixelStrip(object):
    def __init__(self, pin, pixels, channel):
        self.strip = Adafruit_NeoPixel(pixels, pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                                       channel, LED_STRIP)
        self.strip.begin()

    def show(self):
        print("before cur time", time.time())
        self.strip.setPixelColor(0, LED_TURN_ON)
        print("mid cur time", time.time())
        self.strip.show()
        print("after cur time", time.time())

    def run(self):
        self.thread = threading.Thread(target=self.show, args=())
        self.thread.daemon = True
        self.thread.start()

