from sys import exit

try:
    from PIL import Image
except ImportError:
    exit("This script requires this pillow module\nInstall with : sudo pip install pillow")

import threading
import time
from operator import eq

import unicornhathd
from filemgr import FileManager
from signal_interface import Signal


# -------------------- DEFINE LED ------------------ #
LED_TYPE_SPRITE = 0
LED_TYPE_BLINK = 1
LED_TYPE_EFFECT = 2
LED_TYPE_NONE = 3

LED_DEFAULT_NAME = "team8_bird"
LED_DEFAULT_SPEED = 0.5
LED_DEFAULT_BRIGHT = 0.5
LED_DEFAULT_ROTATION = 90
LED_DEFAULT_TYPE = LED_TYPE_SPRITE

LED_PASS_ATTRIBUTE = -1

WIDTH, HEIGHT = unicornhathd.get_shape()

LED_SPRITE_FORMAT = '.png'
RESOURCE_DIR = 'res/'

unicornhathd.rotation(LED_DEFAULT_ROTATION)
unicornhathd.brightness(LED_DEFAULT_BRIGHT)

class UnicornLED(object):

    def __init__(self):
        state = FileManager.get_read_state()

        if state is not None:
            for ledState in state['LED_STATE']:
                self._curImageName = ledState['index']
                self._curType = float(ledState['type'])
                self._curSpeed = float(ledState['speed'])
                self._curBright = float(ledState['brightness'])
                unicornhathd.brightness(self._curBright)
        else:
            self._curImageName = LED_DEFAULT_NAME
            self._curType = LED_DEFAULT_TYPE
            self._curSpeed = LED_DEFAULT_SPEED
            self._curBright = LED_DEFAULT_BRIGHT
            unicornhathd.brightness(LED_DEFAULT_BRIGHT)

        self._IsInturrpt = False

    # LED Callback Function
    def set_attribute(self, imagename, type, speed, brightness):
        # set attributes from bluetooth data

        if self._IsInturrpt is True:
            return

        if imagename != LED_PASS_ATTRIBUTE:
            self._curImageName = imagename

        if type != LED_PASS_ATTRIBUTE:
            self._curType = type

        if speed != LED_PASS_ATTRIBUTE:
            self._curSpeed = speed

        if brightness != LED_PASS_ATTRIBUTE:
            self._curBright = brightness
            unicornhathd.brightness(brightness)

        obj_LED = {}
        obj_LED['LED_STATE'] = []
        obj_LED['LED_STATE'].append({
            'index': self._curImageName,
            'type': self._curType,
            'speed': self._curSpeed,
            'brightness': self._curBright
        })

        FileManager.save_state(obj_LED)

    def get_led_info(self):
        return "info" + Signal.READ_BYTE_SEPARATE + \
               str(self._curImageName) + Signal.READ_BYTE_SEPARATE + \
               str(self._curSpeed) + Signal.READ_BYTE_SEPARATE + \
               str(self._curBright)

    def blink_LED(self):
        unicornhathd.show()
        time.sleep(0.5)
        unicornhathd.off()
        time.sleep(0.3)

    def show_LED(self, imagename, targetImage, type):
        # if self._IsInturrpt is True:
        #     imagename = self._interruptImageName
        #     targetImage = Image.open(RESOURCE_DIR + self._interruptImageName + LED_SPRITE_FORMAT)
        #     type = self._interruptImageType

        for o_x in range(int(targetImage.size[0] / WIDTH)):
            for o_y in range(int(targetImage.size[1] / HEIGHT)):
                valid = False

                # if signal not equal, Interrupt LED!
                # if self._IsInturrpt is True:
                #     if imagename == LED_LEFT_LED_IND or imagename == LED_RIGHT_LED_IND or imagename == LED_EMERGENCY_LED_IND:
                #         pass
                #     else:
                #         break
                # else:
                if not eq(self._curImageName, imagename):
                    break

                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        pixel = targetImage.getpixel(((o_x * WIDTH) + y, (o_y * HEIGHT) + x))
                        r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                        if r or g or b:
                            valid = True
                        unicornhathd.set_pixel(x, y, r, g, b)
                if valid:
                    if eq(type, LED_TYPE_SPRITE):
                        unicornhathd.show()
                        time.sleep(self._curSpeed)

                    elif eq(type, LED_TYPE_BLINK):
                        self.blink_LED()

                    elif eq(type, LED_TYPE_NONE):
                        unicornhathd.show()

    def control_LED(self):
        while True:
            try:
                try:
                    targetImage = Image.open(RESOURCE_DIR + self._curImageName + LED_SPRITE_FORMAT)
                    self.show_LED(self._curImageName, targetImage, self._curType)

                except IOError, e:
                    print "Waiting loading Image (After Download Image)"
                    print e

                except KeyError:
                    print("not exist image")

            except KeyboardInterrupt:
                print("disconnected")
                unicornhathd.off()
                print("receiveMsg KeyboardInterrupt")
                break

    # def inturrpt_LED(self, type):
    #     # print("IsInturrpt is " + type)
    #     self._IsInturrpt = True
    #
    #     if type == "left":
    #         self._interruptImageName = LED_LEFT_LED_IND
    #         self._interruptImageType = LED_TYPE_BLINK
    #     elif type == "right":
    #         self._interruptImageName = LED_RIGHT_LED_IND
    #         self._interruptImageType = LED_TYPE_BLINK
    #     elif type == "emergency":
    #         self._interruptImageName = LED_EMERGENCY_LED_IND
    #         self._interruptImageType = LED_TYPE_BLINK
    #     elif type == "none":
    #         self._IsInturrpt = False

    def run(self):
        t1 = threading.Thread(target=self.control_LED)
        t1.daemon = True
        t1.start()

# END

