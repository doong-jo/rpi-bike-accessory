from bluetooth import *
from filemgr import FileManager
import threading
from signal_interface import Signal
import subprocess

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

# LED
LED_TYPE_SPRITE = 0
LED_PASS_ATTRIBUTE = -1
######################################################


class BluetoothRFCOMM(object):
    def __init__(self):
        self._sendFineState = True
        self._isConnected = False
        self._client_sock = None

    def send_message(self, string):
        if self._isConnected is False:
            return

        if self._sendFineState is False:
            return

        print("try sendMsg" + string)

        try:
            print ("sendMsg Successful")
            self._sendFineState = False
            self._client_sock.send(string)

        except AttributeError:
            print ("sendMsg Attrubute Error")

    def receive_message(self, led_set_attribute, led_get_info, gyro_bluetooth_trigger, file_save_image, file_get_exists):
        while True:
            self._sendFineState = True
            self._isConnected = False

            gyro_bluetooth_trigger(False)

            bitmap_byte_arr_LED = ""
            cur_name_LED = ""

            server_sock = BluetoothSocket(RFCOMM)
            server_sock.bind(('', PORT_ANY))
            server_sock.listen(1)

            port = server_sock.getsockname()[1]

            advertise_service(server_sock, "helperService",
                              service_id=BT_UUID,
                              service_classes=[BT_UUID, SERIAL_PORT_CLASS],
                              profiles=[SERIAL_PORT_PROFILE])

            print("Waiting for connection : channel %d" % port)
            self._client_sock, client_info = server_sock.accept()

            print("Accepted connection from ", client_info)
            subprocess.call(['sudo', 'bluetoothctl', 'discoverable', 'no'])

            while True:
                try:
                    print("Wating for recv")
                    data = self._client_sock.recv(BT_SIZE_READ_BYTE)
                    print("data length : ", len(data))
                    print("data : %s", data)

                    split_data = data.split(BT_READ_BYTE_SEPARATE)
                    signal_data = split_data[0]

                    if signal_data == BT_SIGNAL_ASK_LED:
                        print("ASK_LED")
                        value_data = split_data[1]

                        cur_name_LED = value_data
                        exists = file_get_exists(cur_name_LED)

                        if exists:
                            exists = BT_SIGNAL_RES_EXIST_LED
                            led_set_attribute(cur_name_LED, LED_TYPE_SPRITE, LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE)
                        else:
                            exists = BT_SIGNAL_RES_DOWNLOAD_LED

                        self.send_message(
                            BT_SIGNAL_RESPONSE_LED +
                            BT_READ_BYTE_SEPARATE +
                            exists
                        )

                    elif signal_data == BT_SIGNAL_DOWNLOAD_LED:
                        print("DOWNLOAD LED")
                        value_data = split_data[1]

                        if bitmap_byte_arr_LED == "":
                            # print("first insert bytearray")
                            bitmap_byte_arr_LED = bytearray(value_data)
                            # print("bitmap_byte_arr_LED length : ", len(bitmap_byte_arr_LED))

                        else:
                            # print("after insert bytearray")
                            appendByteArr = bytearray(value_data)
                            bitmap_byte_arr_LED = bitmap_byte_arr_LED + appendByteArr
                            # print("bitmap_byte_arr_LED length : ", len(bitmap_byte_arr_LED))

                        self.send_message(
                            BT_SIGNAL_DOWNLOAD_LED
                        )

                    elif signal_data == BT_SIGNAL_DOWNLOAD_DONE_LED:
                        # print("DONE DOWNLOAD LED")
                        # print("final bitmap_byte_arr_LED length : ", len(bitmap_byte_arr_LED))
                        file_save_image(cur_name_LED, bitmap_byte_arr_LED)
                        bitmap_byte_arr_LED = ""
                        led_set_attribute(cur_name_LED, LED_TYPE_SPRITE, LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE)

                    elif signal_data == BT_SIGNAL_SPEED:
                        # print("ADJUST SPEED")
                        value_data = int(split_data[1].split(BT_SIGNAL_SPEED)[0])
                        led_set_attribute(LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE, value_data * 0.1, LED_PASS_ATTRIBUTE)

                    elif signal_data == BT_SIGNAL_BRIGHTNESS:
                        # print("ADJUST BRIGHTNESS")
                        value_data = int(split_data[1].split(BT_SIGNAL_BRIGHTNESS)[0])
                        print "bright value : " + (str)(value_data)
                        led_set_attribute(LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE, value_data * 0.1)
                    
                    elif signal_data == BT_SIGNAL_RES:
                        self._sendFineState = True

                    elif signal_data == Signal.RES:
                        BluetoothRFCOMM.sendFineState = True

                    elif signal_data == Signal.CONNECTED:
                        BluetoothRFCOMM.isConnected = True
                        self.send_message(led_get_info())

                        gyro_bluetooth_trigger(True)
                        # print("receive connect signal")

                except IOError:
                    print("disconnected")
                    self._client_sock.close()
                    server_sock.close()
                    break

                except KeyboardInterrupt:
                    print("receiveMsg KeyboardInterrupt")
                    self._client_sock.close()
                    server_sock.close()
                    break

    def run(self, led_set_attribute, led_get_info, gyro_bluetooth_trigger, save_image, get_exists):
        t1 = threading.Thread(target=self.receive_message,
                              args=(led_set_attribute,
                                    led_get_info,
                                    gyro_bluetooth_trigger,
                                    save_image,
                                    get_exists))
        t1.daemon = True
        t1.start()
