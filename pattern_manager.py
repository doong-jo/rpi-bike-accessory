import time
from neopixel import *

SECOND_TO_MS = 1000.0
SPEED = 250.0

LED_TURN_ON     = Color(255, 0, 0)
LED_TURN_OFF    = Color(0, 0, 0)


class PatternMgr(object):
    TIC_TOK = 0,
    CONTINUOUS = 1,
    FADE_OUT = 2,

    patternIdx = 0
    ledNum = 0
    ledCurIndex = []
    ledBrightnessArr = []
    strips = []
    break_trigger = False

    @staticmethod
    def interrupt_show():
        for strip in PatternMgr.strips:
            strip.interrupt_show()

    @staticmethod
    def run():
        for strip in PatternMgr.strips:
            strip.run()

    @staticmethod
    def clear():
        for strip in PatternMgr.strips:
            strip.set_clear()

    @staticmethod
    def join():
        for strip in PatternMgr.strips:
            strip.get_thread().join()

    @staticmethod
    def set_break_trigger(trigger):
        PatternMgr.break_trigger = trigger

    @staticmethod
    def led_off():
        PatternMgr.join()
        PatternMgr.clear()

    @staticmethod
    def add_led(_ledPin, strip):
        PatternMgr.ledCurIndex.append(
            {str(_ledPin): 0})

        PatternMgr.strips.append(strip)

    @staticmethod
    def set_led_trigger(val):
        PatternMgr.ledTrigger = val

    @staticmethod
    def set_pattern(_patternIdx):
        PatternMgr.patternIdx = _patternIdx

    @staticmethod
    def set_value_dic(val, arr):
        for obj in arr:
            key = str(obj.keys()[0])
            obj[key] = val

    @staticmethod
    def find_object(keyName, arr):
        i = 0
        for obj in arr:
            key = str(obj.keys()[0])

            if key == str(keyName):
                return i
            i = i + 1

    @staticmethod
    def get_pattern():

        return {
            'type': PatternMgr.patterns[PatternMgr.patternIdx]['type'],
            'func': PatternMgr.patterns[PatternMgr.patternIdx]['func']
        }

    @staticmethod
    def colorWipe(strip, color):
        for i in range(strip.numPixels()):
            if PatternMgr.break_trigger is True:
                break
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep((1.0 / (strip.numPixels()) * 2.5) * SPEED / SECOND_TO_MS)

    @staticmethod
    def fast_Wipe(strip, color):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            if PatternMgr.break_trigger is True:
                break
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(( 1.0 / (strip.numPixels())) * SPEED / SECOND_TO_MS)

    @staticmethod
    def wipetomiddle(strip, color):
        """Wipe color across display a pixel at a time."""

        for i in range(((strip.numPixels()) / 2)):
            if PatternMgr.break_trigger is True:
                break
            strip.setPixelColor(i, color)
            strip.setPixelColor(strip.numPixels() - i - 1, color)
            strip.show()
            time.sleep((SPEED / strip.numPixels())/ SECOND_TO_MS)

    @staticmethod
    def theaterChase(strip, color):
        """Movie theater light style chaser animation."""
        for j in range(1):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    if PatternMgr.break_trigger is True:
                        break
                    strip.setPixelColor(i+q, color)
                strip.show()
                time.sleep(SPEED / (5 * SECOND_TO_MS))

                for i in range(0, strip.numPixels(), 3):
                    if PatternMgr.break_trigger is True:
                        break
                    strip.setPixelColor(i+q, 0)
                    # strip.show()

    @staticmethod
    def slowly_turning_on(strip, color):
        """slowly turning on led animation."""
        i = 0
        lightspeed = 1
        sleeping_time = 5 / (strip.numPixels() * strip.numPixels() )

        if color == LED_TURN_OFF:
            lightspeed = -lightspeed
            i = 255

        while True:
            if PatternMgr.break_trigger is True:
                break
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(i, 0, 0))
            strip.show()
            time.sleep(sleeping_time)
            i += lightspeed

            if i == 255 or i == 0:
                break

    @staticmethod
    def slowly_turning_on_one(strip, color):
        """slowly turning on led animation."""
        i = 0
        lightspeed = 5

        pin = strip.get_pin()
        arrCurIdx = PatternMgr.find_object(str(pin), PatternMgr.ledCurIndex)
        curIdxValue = PatternMgr.ledCurIndex[arrCurIdx][str(pin)]
        j = curIdxValue
        sleeping_time = 100 / (SECOND_TO_MS * strip.numPixels() * strip.numPixels()
                               * strip.numPixels() * strip.numPixels())
        if color == LED_TURN_OFF:
            lightspeed = -lightspeed
            i = 255

            PatternMgr.ledCurIndex[arrCurIdx][str(pin)] = PatternMgr.ledCurIndex[arrCurIdx][str(pin)] \
                                                          + (strip.numPixels() / 8)

        while True:
            for t in range(strip.numPixels() / 4):
                if PatternMgr.break_trigger is True:
                    break

                strip.setPixelColor((j + t) % strip.numPixels(), Color(i, 0, 0))
            strip.show()
            time.sleep(sleeping_time)
            i += lightspeed

            if i == 255 or i == 0:
                break

    @staticmethod
    def jump(strip, color):
        """Wipe color across display a pixel at a time."""
        i = 0
        lightspeed = 2

        while i < strip.numPixels():
            strip.setPixelColor(i, color)
            strip.show()

            time.sleep((1.0 / (strip.numPixels()) * 2) * (SPEED*10) / SECOND_TO_MS)
            i += lightspeed

            if i >= strip.numPixels() or i <= 0:
                break

    @staticmethod
    def audi(strip, color):
        """Wipe color across display a pixel at a time."""
        for cnt in range(0, 3):
            if PatternMgr.break_trigger is True:
                break

            i = 0
            sleeping_time = (3.0 / (strip.numPixels()) * 2) * SPEED / SECOND_TO_MS
            if len(PatternMgr.ledBrightnessArr) != 24:
                for j in range(0, 255, 11):
                    if PatternMgr.break_trigger is True:
                        break
                    PatternMgr.ledBrightnessArr.append(j)

            while i <= strip.numPixels():
                if PatternMgr.break_trigger is True:
                    break
                strip.setPixelColor(i, Color(PatternMgr.ledBrightnessArr[i % strip.numPixels()], 0, 0))
                strip.setPixelColor(i + 1, Color(PatternMgr.ledBrightnessArr[(i+1) % strip.numPixels()], 0, 0))
                strip.setPixelColor(i + 2, Color(PatternMgr.ledBrightnessArr[(i + 2) % strip.numPixels()], 0, 0))
                strip.setPixelColor(i + 3, Color(PatternMgr.ledBrightnessArr[(i + 2) % strip.numPixels()], 0, 0))
                strip.setPixelColor(i + 4, Color(PatternMgr.ledBrightnessArr[(i + 2) % strip.numPixels()], 0, 0))
                strip.setPixelColor(i - 2, Color(0, 0, 0))
                strip.setPixelColor(i - 1, Color(0, 0, 0))
                strip.show()
                time.sleep(sleeping_time)
                i += 2

            i = strip.numPixels() - 1
            while i >= 1 :
                if PatternMgr.break_trigger is True:
                    break
                strip.setPixelColor(i, Color(PatternMgr.ledBrightnessArr[i], 0, 0))
                strip.show()
                time.sleep(sleeping_time)
                i -= 2
            #
            i = strip.numPixels() - 1
            while i >= 1 :
                if PatternMgr.break_trigger is True:
                    break
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
                time.sleep(sleeping_time)
                i -= 2
            while i <= strip.numPixels() :
                if PatternMgr.break_trigger is True:
                    break
                strip.setPixelColor(i, color)
                strip.setPixelColor(i - 1, Color(0, 0, 0))
                strip.show()
                time.sleep(sleeping_time)
                i += 1

            time.sleep(1)

    @staticmethod
    def catching_tail(strip, color):
        for cnt in range(0, 10):
            i = 0
            r = 0

            while (r !=  strip.numPixels()) :
                if PatternMgr.break_trigger is True:
                    break

                strip.setPixelColor(i % strip.numPixels(), color)
                strip.setPixelColor((i + 1) % strip.numPixels(), color)
                strip.setPixelColor((i + 2) % strip.numPixels(), color)
                strip.setPixelColor((i + strip.numPixels() - 1) % strip.numPixels(), Color(0, 0, 0))
                strip.show()
                time.sleep((5.0 / (strip.numPixels() * 2) * SPEED / SECOND_TO_MS))
                i += 1
                i = i % strip.numPixels()
                r += 1

    @staticmethod
    def side_on_L(strip, color):
        r = strip.numPixels() / 2
        for t in range(r):
            strip.setPixelColor(t % strip.numPixels(), color)
        strip.show()
        time.sleep(0.5)
        for t in range(r):
            strip.setPixelColor(t % strip.numPixels(), Color(0, 0, 0))
        strip.show()

    @staticmethod
    def side_on_R(strip, color):
        r = strip.numPixels() / 2
        for t in range(r, strip.numPixels()):
            strip.setPixelColor(t % strip.numPixels(), color)
        strip.show()
        time.sleep(0.5)
        for t in range(r, strip.numPixels()):
            strip.setPixelColor(t % strip.numPixels(), Color(0, 0, 0))
        strip.show()

    @staticmethod
    def side_empty(strip, color):
        """side lights on / off"""
        half_r = strip.numPixels() / 2
        quarter_r = strip.numPixels() / 4
        i = LED_TURN_OFF
        t = 0
        k = 0
        for w in range(strip.numPixels()):
            if PatternMgr.break_trigger is True:
                break

            strip.setPixelColor(w, color)
            strip.show()
            time.sleep(0.001)
        while True:
            if i == color:
                i = LED_TURN_OFF
            else:
                i = color

            for t in range(-1, 2, 1):
                if PatternMgr.break_trigger is True:
                    break

                strip.setPixelColor((quarter_r + t), i)
                strip.setPixelColor((half_r + quarter_r + t), i)
            strip.show()
            time.sleep(0.3)

    @staticmethod
    def rotating_two(strip, color):
        """tail breaking light on."""
        for cnt in range(0, 10):
            r = strip.numPixels() / 2
            i = 0

            while i != strip.numPixels():
                if PatternMgr.break_trigger is True:
                    break

                strip.setPixelColor((i) % strip.numPixels(), color)
                strip.setPixelColor((i + 1) % strip.numPixels(), color)
                strip.setPixelColor((r + i) % strip.numPixels(), color)
                strip.setPixelColor((r + i + 1) % strip.numPixels(), color)
                strip.show()
                time.sleep(0.01)
                strip.setPixelColor((i) % strip.numPixels(), LED_TURN_OFF)
                strip.setPixelColor((r + i) % strip.numPixels(), LED_TURN_OFF)
                strip.show()
                i += 1

    @staticmethod
    def rotating_half(strip, color):
        """tail breaking light on."""
        r = strip.numPixels() / 2
        i = 0
        lightspeed = 1
        if color is LED_TURN_OFF:
            lightspeed = -lightspeed
        while i != strip.numPixels():
            if PatternMgr.break_trigger is True:
                break

            strip.setPixelColor(i % strip.numPixels(), color)
            strip.setPixelColor((i + 1) % strip.numPixels(), color)
            strip.setPixelColor((r + i) % strip.numPixels(), color)
            strip.setPixelColor((r + i + 1) % strip.numPixels(), color)
            strip.show()
            time.sleep(0.01)
            i += lightspeed
            if i == -2 * r:
                break

    @staticmethod
    def cross_light(strip, color):
        """side lights on / off"""

        i = 0
        sleeping_time = (3.0 / (strip.numPixels()) * 2) * SPEED / SECOND_TO_MS
        if len(PatternMgr.ledBrightnessArr) != 24:
            for j in range(0, 255, 11):
                if PatternMgr.break_trigger is True:
                    break
                PatternMgr.ledBrightnessArr.append(j)

            for t in range(7):
                if PatternMgr.break_trigger is True:
                    break
                strip.setPixelColor((i + t) % strip.numPixels(), Color(PatternMgr.ledBrightnessArr[3 + t*3], 0, 0))
            strip.setPixelColor((i - 1) % strip.numPixels(), Color(0, 0, 0))
            strip.setPixelColor((i - 2) % strip.numPixels(), Color(0, 0, 0))
            strip.show()
            time.sleep(sleeping_time)
            i += 2

    @staticmethod
    def meteor(strip, color):
        """side lights on / off"""
        lightspeed_1 = 1
        lightspeed_2 = 2
        # if lightspeed_2 is 3, then new pattern will be created

        i = 0
        j = 0

        for cnt in range(0, 100):
            if PatternMgr.break_trigger is True:
                break

            i = (i + lightspeed_1) % strip.numPixels()
            j = (j + lightspeed_2) % strip.numPixels()

            strip.setPixelColor(i, LED_TURN_OFF)
            for t in range(0, 2):
                strip.setPixelColor((j % strip.numPixels() - t)% strip.numPixels(), LED_TURN_OFF)
            strip.setPixelColor((i + lightspeed_1) % strip.numPixels(), color)
            for t in range(0, 3):
                strip.setPixelColor((j + lightspeed_2 + t) % strip.numPixels(), color)
            strip.show()
            time.sleep(0.05)

    @staticmethod
    def eating(strip, color):
        """side lights on / off"""
        lightspeed_1 = int(round(float(strip.numPixels()) / 10.0, 1))
        lightspeed_2 = int(round(float(strip.numPixels()) * 2.0 / 10.0, 1))
        # if lightspeed_2 is 3, then new pattern will be created

        i = 0
        j = 0
        k = 0
        on = color
        off = LED_TURN_OFF
        if color == LED_TURN_OFF:
            on = LED_TURN_OFF
            off = color

        while True and (k != strip.numPixels()):
            if PatternMgr.break_trigger is True:
                break

            i = (i + lightspeed_1) % strip.numPixels()
            j = (j + lightspeed_2) % strip.numPixels()

            strip.setPixelColor(i, off)
            for t in range(0, 2):
                strip.setPixelColor((j % strip.numPixels() - t) % strip.numPixels(), off)
            strip.setPixelColor((i + lightspeed_1) % strip.numPixels(), on)
            for t in range(0, k):
                strip.setPixelColor((j + lightspeed_2 + t) % strip.numPixels(), on)
            strip.show()
            time.sleep((10.0 / (strip.numPixels()) * SPEED / SECOND_TO_MS))
            if j == 0:
                k += 1

    @staticmethod
    def quarter(strip, color):
        """tail breaking light on."""
        ledarray=[0, 2, 1, 3]
        quarter = strip.numPixels() / 4
        for i in ledarray:
            for j in range(strip.numPixels() / 4):
                strip.setPixelColor(i * quarter + j, color)
            time.sleep(0.2)
            strip.show()

    @staticmethod
    def vane_pattern(strip, color):
        """tail breaking light on."""
        k = 0
        quarter = strip.numPixels() / 4
        for cnt in range(0, 100):
            for i in range(strip.numPixels()):
                for j in range(strip.numPixels() / 8):
                    if PatternMgr.break_trigger is True:
                        break

                    strip.setPixelColor((i * quarter + j + k) % strip.numPixels(), color)
                strip.setPixelColor((i * quarter - 1 + k) % strip.numPixels(), LED_TURN_OFF)
            strip.show()
            time.sleep((1.0 / (strip.numPixels()) * SPEED / SECOND_TO_MS))
            k = (k + 1) % strip.numPixels()

    @staticmethod
    def break_on(strip, color):
        """tail breaking light on."""
        for i in range(strip.numPixels()):
            if PatternMgr.break_trigger is True:
                break

            strip.setPixelColor(i, LED_TURN_ON)
        strip.show()

    @staticmethod
    def set_clear(strip, color):
        """tail breaking light on."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, LED_TURN_OFF)
        strip.show()
        time.sleep(0.3)

    #
    # @staticmethod
    # def vane_pattern(strip, color):
    #     i = 0
    #     r = 0
    #     t = strip.numPixels() / 4
    #     sleeping_time =(1.0 / (strip.numPixels() * strip.numPixels() * strip.numPixels() *  2) * SPEED)
    #     while r !=strip.numPixels():
    #         for t in range(0, strip.numPixels(), strip.numPixels()/4):
    #             for q in range(0, strip.numPixels() / 8):
    #                 strip.setPixelColor((t + i % strip.numPixels() + q) , color)
    #             strip.setPixelColor((t + i + strip.numPixels() - 1) % strip.numPixels(), Color(0, 0, 0))
    #             strip.show()
    #         time.sleep(sleeping_time)
    #
    #         i += 1
    #         i = i % strip.numPixels()
    #         r += 1

PatternMgr.patterns = [
    {'func': PatternMgr.colorWipe, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.fast_Wipe, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.wipetomiddle, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.theaterChase, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.slowly_turning_on, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.slowly_turning_on_one, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.side_on_L, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.side_on_R, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.jump, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.audi, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.catching_tail, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.side_empty, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.rotating_two, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.rotating_half, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.cross_light, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.meteor, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.eating, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.quarter, 'type': PatternMgr.TIC_TOK},
    {'func': PatternMgr.vane_pattern, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.break_on, 'type': PatternMgr.CONTINUOUS},
    {'func': PatternMgr.set_clear, 'type': PatternMgr.CONTINUOUS}


]
