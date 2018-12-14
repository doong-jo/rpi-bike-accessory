import json
import os

try:
    from PIL import Image, ImageFile
except ImportError:
    exit("This script requires this pillow module\nInstall with : sudo pip install pillow")

# -------------------- DEFINE FILE ------------------ #
FILE_STATE_JSON_NAME = "state.json"
FILE_COLLISION_LOG_NAME = "pattern.txt"
FILE_COLLISION_PATTERN = "./logs/common_shock.txt"
FILE_DIR_RESOURCE = "./res/"
FILE_FORMAT_LED_IMAGE = ".png"
#######################################################


class FileManager(object):
    def __init__(self):
        pass

    @staticmethod
    def get_collision_model():
        try:
            with open(FILE_COLLISION_PATTERN, mode='rt', buffering=1024) as fileContent:
                data_arr = []
                for line in fileContent:
                    try:
                        data_arr.append(line)
                    except IndexError:
                        break
                return data_arr
        except IOError, e:
            print e

    @staticmethod
    def save_state(dic_data):
        with open(FILE_STATE_JSON_NAME, 'w') as outfile:
            json.dump(dic_data, outfile)

    ######################FOR TEST######################
    @staticmethod
    def save_append_collision_log(data):
        with open(FILE_COLLISION_LOG_NAME, 'a') as outfile:
            outfile.write((str)(data['date']) + ", ")
            outfile.write((str)(data['accel'])+ ", ")
            outfile.write((str)(data['angle_x']) + "\n")
    ####################################################

    @staticmethod
    def get_read_state():
        state_dic = ""

        try:
            with open(FILE_STATE_JSON_NAME, 'r') as f:
                state_dic = json.load(f)
        except ValueError, e:
            print e
            return "team8_bird"

        except IOError, e:
            print e

        return state_dic

    @staticmethod
    def get_exists_LED(led_name):
        return os.path.exists(FILE_DIR_RESOURCE + led_name + FILE_FORMAT_LED_IMAGE)

    @staticmethod
    def save_image_LED(file_name, bitmap_byte_arr):
        file_name = "./res/" + file_name + FILE_FORMAT_LED_IMAGE

        try:
            image_file = open(file_name, "wb")
            image_file.write(bitmap_byte_arr)
            image_file.close()

        except IOError, e:
            print e
