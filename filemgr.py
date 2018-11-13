import json
import os
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

        imageFile = open(fileName, "wb")
        imageFile.write(bitmapByteArr)
        imageFile.close()

    # def saveImage(self):
        # pass

