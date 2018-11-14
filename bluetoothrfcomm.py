from bluetooth import *
from filemgr import FileManager
import threading
import time

# DEFINE SIGNAL_INDEX
# LED           0
# SPEED         1
# BRIGHTNESS    2
# CLOSE         -1

# - : splite word

# LED
# SIGNAL_INDEX-LED_INDEX-TYPE(SPRITE, BLINK, EFFECT)#
# LED example : 0-01-0 (LED-01st-LED-SPRITE => LED 1 sprite)

# SPEED
# SIGNAL_INDEX-SPEED#
# SPEED example : 1-05-0 (0~10) (SPEED-5 => frame speed = interval 0.5 sec)

# BRIGHTNESS
# SIGNAL_INDEX-BRIGHTNESS#
# BRIGHTNESS example : 2-05-0 (0~10) (BRIGHTNESS-5 => brightness level 5)


# ----------- DEFINE BLUETOOTH ATTRIBUTE ----------- #
BT_SIZE_READ_BYTE = 1024
BT_UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

# SIGNAL
BT_SIGNAL_ASK_LED = "AL"
BT_SIGNAL_RESPONSE_LED = "RL"
BT_SIGNAL_RES_DOWNLOAD_LED = "RDL"
BT_SIGNAL_RES_EXIST_LED = "REL"
BT_SIGNAL_DOWNLOAD_LED = "DL"
BT_SIGNAL_DOWNLOAD_DONE_LED = "DDL"

BT_SIGNAL_BRIGHTNESS = "B"
BT_SIGNAL_SPEED = "S"

BT_READ_BYTE_SEPARATE = "!S!"

# LED OPTIONAL
LED_TYPE_SPRITE = 0
######################################################



g_client_sock = None

class BluetoothRFCOMM(object):
    def __init__(self):
        pass

    def sendMsg(self, string):
        global g_client_sock

        print("try sendMsg" + string)

        try:
            print ("sendMsg Successful")
            g_client_sock.send(string)
        except AttributeError:
            print ("sendMsg Attrubute Error")


    def receiveMsg(self, ledcb, ledinfocb):
        while True:

            global g_client_sock
            global ledName
            global ledBitmapByteArr

            server_sock = BluetoothSocket(RFCOMM)
            server_sock.bind(('', PORT_ANY))
            server_sock.listen(1)

            port = server_sock.getsockname()[1]

            advertise_service(server_sock, "helperService",
                              service_id=BT_UUID,
                              service_classes=[BT_UUID, SERIAL_PORT_CLASS],
                              profiles=[SERIAL_PORT_PROFILE])

            ledBitmapByteArr = ""
            ledFileName = ""

            print("Waiting for connection : channel %d" % port)
            g_client_sock, client_info = server_sock.accept()

            print("Accepted connection from ", client_info)

            self.sendMsg(ledinfocb())

            while True:
                try:
                    print("Wating for recv")
                    data = g_client_sock.recv(BT_SIZE_READ_BYTE)
                    print("data length : ", len(data))
                    print("data : %s", data)

                    splitData = data.split(BT_READ_BYTE_SEPARATE)
                    signalData = splitData[0]

                    if signalData == BT_SIGNAL_ASK_LED:
                        print("ASK_LED")
                        valueData = splitData[1]

                        ledName = valueData
                        exists = FileManager.getExistsResourceLED(ledName)

                        if exists:
                            exists = BT_SIGNAL_RES_EXIST_LED
                            ledcb(ledName, LED_TYPE_SPRITE, -1, -1)
                        else:
                            exists = BT_SIGNAL_RES_DOWNLOAD_LED

                        self.sendMsg(
                            BT_SIGNAL_RESPONSE_LED +
                            BT_READ_BYTE_SEPARATE +
                            exists
                        )

                    elif signalData == BT_SIGNAL_DOWNLOAD_LED:
                        print("DOWNLAOD LED")
                        valueData = splitData[1]

                        if ledBitmapByteArr == "":
                            print("first insert bytearray")
                            ledBitmapByteArr = bytearray(valueData)
                            print("ledBitmapByteArr length : ", len(ledBitmapByteArr))

                        else:
                            print("after insert bytearray")
                            appendByteArr = bytearray(valueData)
                            ledBitmapByteArr = ledBitmapByteArr + appendByteArr
                            print("ledBitmapByteArr length : ", len(ledBitmapByteArr))

                        self.sendMsg(
                            BT_SIGNAL_DOWNLOAD_LED
                        )

                    elif signalData == BT_SIGNAL_DOWNLOAD_DONE_LED:
                        print("DONE DOWNLOAD LED")
                        print("final ledBitmapByteArr length : ", len(ledBitmapByteArr))
                        FileManager.saveResourceLED(ledName, ledBitmapByteArr)
                        ledBitmapByteArr = ""
                        ledcb(ledName, LED_TYPE_SPRITE, -1, -1)

                    elif signalData == BT_SIGNAL_SPEED:
                        print("ADJUST SPEED")
                        valueData = int(splitData[1])
                        ledcb(-1, -1, valueData * 0.1, -1)

                    elif signalData == BT_SIGNAL_BRIGHTNESS:
                        print("ADJUST BRIGHTNESS")
                        valueData = int(splitData[1])
                        ledcb(-1, -1, -1, valueData * 0.1)

                    # try:
                    #     signalData = int(splitData[0])
                    #
                    #     if signalData == 3:
                    #         valueData = splitData[1]
                    #         optionalData = splitData[2]
                    #     else:
                    #         valueData = int(splitData[1])
                    #         optionalData = int(splitData[2])
                    #
                    # except KeyError:
                    #     pass
                    #
                    # if signalData == 0:
                    #     ledcb(valueData, optionalData, -1, -1)
                    #
                    # elif signalData == 1:
                    #     ledcb(-1, -1, valueData * 0.1 + optionalData * 0.01, -1)
                    #
                    # elif signalData == 2:
                    #     ledcb(-1, -1, -1, valueData * 0.1 + optionalData * 0.01)
                    #
                    # elif signalData == 3:
                    #     # optionalData : imageName (bird.png)
                    #     # valueData : byteArray of Bitmap from App
                    #     fileName = "./res/" + optionalData
                    #     imageName = optionalData.split('.')[0]
                    #
                    #     imageFile = open(fileName, "wb")
                    #     imageFile.write(valueData)
                    #     imageFile.close()
                    #
                    #     ledcb(imageName, 0, -1, -1)

                except IOError:
                    print("disconnected")
                    g_client_sock.close()
                    server_sock.close()
                    break

                except KeyboardInterrupt:
                    print("receiveMsg KeyboardInterrupt")
                    g_client_sock.close()
                    server_sock.close()
                    break


    def run(self, ledcb, ledinfocb):
        t1 = threading.Thread(target=self.receiveMsg, args=(ledcb, ledinfocb, ))
        t1.daemon = True
        t1.start()
