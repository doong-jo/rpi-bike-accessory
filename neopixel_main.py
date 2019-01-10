import time
from button import Button
from gyroscope import Mpu
# from SPI_Connection import State_of_Charge
# from Circular_LED import led_pattern
from test_neopixel_strip import NeopixelStrip
from pattern_manager import PatternMgr
from pattern_interface import Pattern
from velocity_corner import vel_corner

def main():
    out_strip = NeopixelStrip(13, 24, 1)

    try:
        out_strip.run()

    except KeyboardInterrupt:
        print("main KeyboardInterrupt")

    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("main KeyboardInterrupt")


if __name__ == '__main__':
    main()
