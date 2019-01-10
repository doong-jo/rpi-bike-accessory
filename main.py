import time
from button import Button
from gyroscope import Mpu
from spi_connection import State_of_Charge
from neopixel_strip import NeopixelStrip
from pattern_manager import PatternMgr
from pattern_interface import Pattern

PATTERN_SLEEP_MS = 2

GOOD_PATTERN = [
    Pattern.AUDI_PATTERN_LIGHTS,
    Pattern.CATCHING_TAIL,
    Pattern.ROTATING_TWO,
    Pattern.METEOR_LIGHT,
    Pattern.EATING_LIGHT,
    Pattern.VANE_PATTERN,
]

def main():
    button = Button()
    mpu = Mpu()

    in_strip = NeopixelStrip(12, 16, 0)
    out_strip = NeopixelStrip(13, 24, 1)

    PatternMgr.add_led(12, out_strip)
    PatternMgr.add_led(13, in_strip)

    try:
        mpu.run()
        button.run()

        idx = 0

        while True:
            while idx < len(GOOD_PATTERN):
                if Mpu.get_inturrptGyro() is True:
                    PatternMgr.interrupt_show()
                    time.sleep(0.1)
                    continue

                PatternMgr.clear()
                time.sleep(0.3)

                print("led index : ", idx)
                PatternMgr.set_pattern(GOOD_PATTERN[idx])
                PatternMgr.run()
                PatternMgr.join()

                while (out_strip.get_thread().is_alive() or in_strip.get_thread().is_alive()) \
                        and Mpu.get_inturrptGyro() is False:
                    pass

                idx = idx + 1

            if Mpu.get_inturrptGyro() is False:
                idx = 0

    except KeyboardInterrupt:
        print("main KeyboardInterrupt")

    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("main KeyboardInterrupt")


if __name__ == '__main__':
    main()
