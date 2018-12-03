import json
import os

try:
    from PIL import Image, ImageFile
except ImportError:
    exit("This script requires this pillow module\nInstall with : sudo pip install pillow")

# -------------------- DEFINE FILE ------------------ #
FILE_STATE_JSON_NAME = "state.json"
FILE_DIR_RESOURCE = "./res/"
FILE_FORMAT_LED_IMAGE = ".png"
#######################################################


class FileManager(object):
    def __init__(self):
        pass

    def save_state(self, dic_data):
        with open(FILE_STATE_JSON_NAME, 'w') as outfile:
            json.dump(dic_data, outfile)

    def read_state(self):
        state_dic = None

        try:
            with open(FILE_STATE_JSON_NAME, 'r') as f:
                state_dic = json.load(f)
        except ValueError:
            return None

        return state_dic

    def get_exists_LED(self, led_name):
        return os.path.exists(FILE_DIR_RESOURCE + led_name + FILE_FORMAT_LED_IMAGE)

    def save_image_LED(self, file_name, bitmap_byte_arr):
        file_name = "./res/" + file_name + FILE_FORMAT_LED_IMAGE

        print("saveResourceLED/fileName : ", file_name)
        print("bitmapByteArr len : ", len(bitmap_byte_arr))

        try:
            image_file = open(file_name, "wb")
            image_file.write(bitmap_byte_arr)
            image_file.close()
            print "Complete Save!!"

        except IOError, e:
            print "Error opening file"
            print e
