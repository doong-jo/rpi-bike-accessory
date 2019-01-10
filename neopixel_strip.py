import threading
from neopixel import *
from pattern_manager import PatternMgr
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

        self.wait_ms = pixels
        self.pin = pin

        self.thread = threading.Thread(target=self.show, args=())

        self.runTrigger = True
        self.clearCmd = False
        self.color = LED_TURN_ON
        self.loop_cnt = 1

    def get_thread(self):
        return self.thread

    def interrupt_show(self):
        for i in range(0, self.strip.numPixels()):
            self.strip.setPixelColor(i, LED_TURN_ON)
        self.strip.show()

    def set_clear(self):
        for i in range(0, self.strip.numPixels()):
            self.strip.setPixelColor(i, LED_TURN_OFF)
        self.strip.show()

    def set_clear_command(self):
        self.clearCmd = True

    def run_pattern(self):
        pattern_func = PatternMgr.get_pattern()['func']
        pattern_type = PatternMgr.get_pattern()['type']
        if pattern_type == PatternMgr.TIC_TOK:
            self.loop_cnt = 2
        else:
            self.loop_cnt = 1

        while self.loop_cnt != 0:
            pattern_func(self.strip, self.color)

            self.loop_cnt = self.loop_cnt - 1
            if pattern_type == PatternMgr.TIC_TOK:
                self.color = self.color_reverse(self.color)

    def color_reverse(self, color):
        if color is not LED_TURN_OFF:
            color = LED_TURN_OFF
        else:
            color = LED_TURN_ON

        return color

    def show(self):
        self.run_pattern()

    def run(self):
        self.thread = threading.Thread(target=self.show, args=())
        self.thread.daemon = True
        self.thread.start()
