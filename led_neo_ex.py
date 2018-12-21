#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
wait_ms_global = 78


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, direction = 1, wait_ms=wait_ms_global):
    """Wipe color across display a pixel at a time."""
    if direction == 1:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
    if direction == -1:
        i = strip.numPixels()
        while i != 0 :
            i-=1
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)

def fast_Wipe(strip, color, wait_ms=wait_ms_global):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def wipetomiddle(strip, color, index = 1, wait_ms=wait_ms_global, stay_ms=0):
    """Wipe color across display a pixel at a time."""
    i=0
    if index == 1:
        for i in range(((strip.numPixels()) / 2)):
            strip.setPixelColor(i, color)
            strip.setPixelColor(strip.numPixels() - i - 1, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
        time.sleep(0.5)
    if index == -1:
        i = (strip.numPixels()/2) - 1
    while i > -1:
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.setPixelColor(strip.numPixels() - i - 1, Color(0, 0, 0))
        strip.show()
        i -= 1
        time.sleep(wait_ms / 1000.0)
    time.sleep(stay_ms / 1000.0)

def theaterChase(strip, color, wait_ms=wait_ms_global, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def slowly_turning_on(strip, wait_ms=wait_ms_global, lightspeed = 1):
    """slowly turning on led animation."""
    i = 0

    while i < 250:
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, Color(i, i, i))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            i += lightspeed
    while i > 0:
        for j in range(strip.numPixels()):
            i -= lightspeed
            strip.setPixelColor(j, Color(i, i, i))
            strip.show()
            time.sleep(wait_ms / 1000.0)


def slowly_turning_on_one(strip, wait_ms=wait_ms_global, lightspeed = 1):
    """slowly turning on led animation."""
    i=0
    for j in range(strip.numPixels()):
        while i < 250:
            strip.setPixelColor(j, Color(i, i, i))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            i += lightspeed

        while i > 0:
            strip.setPixelColor(j, Color(i, i, i))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            i -= lightspeed

def side_on(strip, color, direction = 1, wait_ms= 1, lightspeed = 1):
    """slowly turning on led animation."""
    i=0
    if direction== 1:
        while i < 250:
            for j in range(strip.numPixels() / 2):
                strip.setPixelColor(j, Color(i, i, i))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                i += lightspeed
        while i > 0:
            for j in range(strip.numPixels() / 2):
                strip.setPixelColor(j, Color(i, i, i))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                i -= lightspeed
    if direction == -1:
        while i < 250:
            for j in range(strip.numPixels() / 2, strip.numPixels()):
                strip.setPixelColor(j, Color(i, i, i))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                i += lightspeed
        while i > 0:
            for j in range(strip.numPixels() / 2, strip.numPixels()):
                strip.setPixelColor(j, Color(i, i, i))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                i -= lightspeed

def jump_lights(strip, odd_even_num, color, wait_ms=wait_ms_global):
    """Wipe color across display a pixel at a time."""
    i=0
    if odd_even_num == 1:
        while i <= strip.numPixels() - 1:
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            i += 2
    if odd_even_num == -1:
        i = strip.numPixels() - 1
        while i >= 1:
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            i -= 2

def Audi_pattern_lights(strip, color, wait_ms = wait_ms_global):
    """Wipe color across display a pixel at a time."""
    i = 0

    while i <= strip.numPixels():
        strip.setPixelColor(i, color)
        strip.setPixelColor(i + 1, color)
        strip.setPixelColor(i - 2, Color(0, 0, 0))
        strip.setPixelColor(i - 1, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        i += 2

    i = strip.numPixels() - 1
    while i >= 1:
        strip.setPixelColor(i, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        i -= 2

    i = strip.numPixels() - 1
    while i >= 1:
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        i -= 2
    while i <= strip.numPixels():
        strip.setPixelColor(i, color)
        strip.setPixelColor(i - 1, Color(0, 0, 0))
        strip.show()
        time.sleep( wait_ms / 1000.0)
        i += 1
    time.sleep(1)

def catching_tail(strip, color, direction = 1,wait_ms = wait_ms_global):
    i = 0
    r = 0
    while r != 5 * strip.numPixels():
        strip.setPixelColor(i % 10, color)
        strip.setPixelColor((i + 1) % 10, color)
        strip.setPixelColor((i + 2) % 10, color)
        strip.setPixelColor((i + 9) % 10, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        i += 1
        if i % 10 == 0:
            r += 1


# Main program logic follows:
def __main__():
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            # print ('1------Color wipe animations.')
            # colorWipe(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS), 1)  # White wipe
            # colorWipe(strip, Color(0, 0, 0), -1)  # turning off wipe
            # time.sleep(1)
            # print ('2------Theater chase animations.')
            # theaterChase(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS))  # White theater chase
            # time.sleep(1)
            # print ("3------Color fast wipe animations.")
            # fast_Wipe(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS),40)
            # time.sleep(1)
            # print ("4------Color wipe to middle animations.")
            # wipetomiddle(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS), 1)
            # wipetomiddle(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS), -1)
            # time.sleep(1)
            # print ("5------slowly light on animations.")
            # slowly_turning_on_one(strip, 0)
            # time.sleep(1)
            # print ("6------slowly light on one by one animations.")
            # slowly_turning_on(strip, 1)
            # time.sleep(1)
            # print ("7------side lights on , 1 left, -1 right")
            # side_on(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS))
            # side_on(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS),-1)
            # time.sleep(1)
            # print("8------jump lights on , 1 odd, -1 even")
            # jump_lights(strip, -1, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS))
            # jump_lights(strip, 1, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS))
            # jump_lights(strip, -1, Color(0, 0, 0))
            # jump_lights(strip, 1, Color(0, 0, 0))
            # time.sleep(1)
            print ("9------Audi_pattern_lights on")
            Audi_pattern_lights(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS),40)
            time.sleep(1)
            # print("10-----catching tail lights on")
            # catching_tail(strip, Color(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS))
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)


__main__()