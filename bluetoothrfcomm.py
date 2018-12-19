from bluetooth import *
from filemgr import FileManager
import threading
from signal_interface import Signal
import subprocess

# ----------- DEFINE BLUETOOTH ATTRIBUTE ----------- #
BT_SIZE_READ_BYTE = 1024
BT_UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


# LED
LED_TYPE_SPRITE = 0
LED_PASS_ATTRIBUTE = -1
######################################################


class BluetoothRFCOMM(object):
    isConnected = False
    sendFineState = False
    clientSock = None

    def __init__(self):
        BluetoothRFCOMM.sendFineState = True
        BluetoothRFCOMM.isConnected = False

    @staticmethod
    def send_message(string):
        if BluetoothRFCOMM.isConnected is False or BluetoothRFCOMM.sendFineState is False:
            return

        print("try sendMsg" + string)

        try:
            print("sendMsg Successful")
            BluetoothRFCOMM.sendFineState = False
            BluetoothRFCOMM.clientSock.send(string)

        except AttributeError:
            print("sendMsg Attrubute Error")

    def receive_message(self,
                        led_set_attribute,
                        led_get_info,
                        gyro_bluetooth_trigger):
        while True:
            BluetoothRFCOMM.sendFineState = True
            BluetoothRFCOMM.isConnected = False

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
            BluetoothRFCOMM.clientSock, client_info = server_sock.accept()

            print("Accepted connection from ", client_info)
            subprocess.call(['sudo', 'bluetoothctl', 'discoverable', 'no'])

            while True:
                try:
                    print("Wating for recv")
                    data = BluetoothRFCOMM.clientSock.recv(BT_SIZE_READ_BYTE)
                    print("data length : ", len(data))
                    print("data : %s", data)

                    split_data = data.split(Signal.READ_BYTE_SEPARATE)
                    signal_data = split_data[0]

                    if signal_data == Signal.ASK_LED:
                        print("ASK_LED")
                        value_data = split_data[1]

                        cur_name_LED = value_data
                        exists = FileManager.get_exists_LED(cur_name_LED)

                        if exists:
                            exists = Signal.RES_EXIST_LED
                            led_set_attribute(cur_name_LED, LED_TYPE_SPRITE, LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE)
                        else:
                            exists = Signal.RES_DOWNLOAD_LED

                        self.send_message(
                            Signal.RESPONSE_LED +
                            Signal.READ_BYTE_SEPARATE +
                            exists
                        )

                    elif signal_data == Signal.DOWNLOAD_LED:
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
                            Signal.DOWNLOAD_LED
                        )

                    elif signal_data == Signal.DOWNLOAD_DONE_LED:
                        # print("DONE DOWNLOAD LED")
                        # print("final bitmap_byte_arr_LED length : ", len(bitmap_byte_arr_LED))
                        FileManager.save_image_LED(cur_name_LED, bitmap_byte_arr_LED)
                        bitmap_byte_arr_LED = ""
                        led_set_attribute(cur_name_LED, LED_TYPE_SPRITE, LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE)

                    elif signal_data == Signal.SPEED:
                        # print("ADJUST SPEED")
                        value_data = int(split_data[1].split(signal_data)[0])
                        led_set_attribute(LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE, value_data * 0.1, LED_PASS_ATTRIBUTE)

                    elif signal_data == Signal.BRIGHTNESS:
                        # print("ADJUST BRIGHTNESS")
                        value_data = int(split_data[1].split(signal_data)[0])
                        print "bright value : " + str(value_data)
                        led_set_attribute(LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE, LED_PASS_ATTRIBUTE, value_data * 0.1)

                    elif signal_data == Signal.THRESHOLD_LEVEL:
                        value_data = str(split_data[1].split(signal_data)[0])
                        print "threshold level : " + str(value_data)

                    elif signal_data == Signal.THRESHOLD_ENABLE:
                        value_data = str(split_data[1].split(signal_data)[0])
                        if value_data == "true":
                            gyro_bluetooth_trigger(True)
                        else:
                            gyro_bluetooth_trigger(False)

                        print "threshold enable : " + str(value_data)

                    elif signal_data == Signal.RES:
                        BluetoothRFCOMM.sendFineState = True

                    elif signal_data == Signal.CONNECTED:
                        BluetoothRFCOMM.isConnected = True
                        self.send_message(led_get_info())

                        gyro_bluetooth_trigger(True)
                        # print("receive connect signal")

                except IOError:
                    print("disconnected")
                    BluetoothRFCOMM.clientSock.close()
                    server_sock.close()
                    break

                except KeyboardInterrupt:
                    print("receiveMsg KeyboardInterrupt")
                    BluetoothRFCOMM.clientSock.close()
                    server_sock.close()
                    break

    def run(self,
            led_set_attribute,
            led_get_info,
            gyro_bluetooth_trigger):
        t1 = threading.Thread(target=self.receive_message,
                              args=(led_set_attribute,
                                    led_get_info,
                                    gyro_bluetooth_trigger,))
        t1.daemon = True
        t1.start()
