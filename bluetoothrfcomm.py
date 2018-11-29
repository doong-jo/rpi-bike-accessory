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

BT_SIGNAL_FILTER = "F"

BT_SIGNAL_RES = "RES"
BT_SIGNAL_CONNECTED = "CONNECTED"

BT_READ_BYTE_SEPARATE = "!S!"

# LED OPTIONAL
LED_TYPE_SPRITE = 0
######################################################



g_client_sock = None

class BluetoothRFCOMM(object):
    def __init__(self):
        self.__sendFineState = True
        self.__isConnected = False
        pass

    def sendMsg(self, string):
        global g_client_sock
        if self.__isConnected is False:
            return

        if self.__sendFineState is False:
            return

        print("try sendMsg" + string)

        try:
            print ("sendMsg Successful")
            self.__sendFineState = False
            g_client_sock.send(string)

        except AttributeError:
            print ("sendMsg Attrubute Error")


    def receiveMsg(self, ledcb, ledinfocb, gyroDataTriggerCb):
        while True:
            self.__sendFineState = True
            self.__isConnected = False

            gyroDataTriggerCb(False)
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
                        valueData = int(splitData[1].split(BT_SIGNAL_SPEED)[0])
                        ledcb(-1, -1, valueData * 0.1, -1)

                    elif signalData == BT_SIGNAL_BRIGHTNESS:
                        print("ADJUST BRIGHTNESS")
                        valueData = int(splitData[1].split(BT_SIGNAL_BRIGHTNESS)[0])
                        ledcb(-1, -1, -1, valueData * 0.1)
                    
                    elif signalData == BT_SIGNAL_RES:
                        self.__sendFineState = True

                    elif signalData == BT_SIGNAL_CONNECTED:
                        self.__isConnected = True
                        self.sendMsg(ledinfocb())

                        gyroDataTriggerCb(True)
                        print("receive connect signal")


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


    def run(self, ledcb, ledinfocb, gyroDataTriggerCb):
        t1 = threading.Thread(target=self.receiveMsg, args=(ledcb, ledinfocb, gyroDataTriggerCb, ))
        t1.daemon = True
        t1.start()
