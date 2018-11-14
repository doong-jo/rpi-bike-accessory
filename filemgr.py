import json
import os
import io
import time

try:
    from PIL import Image, ImageFile
except ImportError:
    exit("This script requires this pillow module\nInstall with : sudo pip install pillow")

# ImageFile.LOAD_TRUNCATED_IMAGES = True
# import Image

# -------------------- DEFINE FILE ------------------ #
FILE_STATE_JSON_NAME = "state.json"
FILE_DIR_RESOURCE = "./res/"
FILE_FORMAT_LED_IMAGE = ".png"
#######################################################


class FileManager(object):
    def __init__(self):
        pass

    def saveLEDState(self, dictionaryData):
        print("saveLEDState")

        with open(FILE_STATE_JSON_NAME, 'w') as outfile:
            json.dump(dictionaryData, outfile)

    def readState(self):

        stateDic = None

        try:
            with open(FILE_STATE_JSON_NAME, 'r') as f:
                stateDic = json.load(f)
        except ValueError:
            return None

        return stateDic

    @staticmethod
    def getExistsResourceLED(ledName):
        return os.path.exists(FILE_DIR_RESOURCE + ledName + FILE_FORMAT_LED_IMAGE)

    @staticmethod
    def saveResourceLED(ledFileName, bitmapByteArr):
        fileName = "./res/" + ledFileName + FILE_FORMAT_LED_IMAGE

        print("saveResourceLED/fileName : ", fileName)
        print("bitmapByteArr len : ", len(bitmapByteArr))

        try:
            # imageFile = Image.open(io.BytesIO(bitmapByteArr))
            imageFile = open(fileName, "wb")
            imageFile.write(bitmapByteArr)
            imageFile.close()
            #time.sleep(10)
            print "Complete Save!!"
            print "Complete Load!!"

        except IOError, e:
            print "Error opening file"

        # imageFile = open(fileName, "wb")
        # imageFile.write(bitmapByteArr)
        # imageFile.close()

    # def saveImage(self):
        # pass

