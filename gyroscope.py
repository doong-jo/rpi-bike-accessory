from mpu6050 import mpu6050
import threading
import math
import datetime
from pytz import timezone
from bluetoothrfcomm import BluetoothRFCOMM
from filemgr import FileManager
from calc import *
from signal_interface import Signal

PASS_ABSOULTE_ACC_AMOUNT = 25
PASS_ROLLOVER_AMOUNT = 40

class Mpu(object):

    def __init__(self):
        self._sensor = mpu6050(0x68)
        self._gyroData = {
            'date': '',
            'similarity': 0.0,
            'accel': 0.0,
            'angle_x': 0.0,
        }
        self._gyroBluetoothSendTrigger = False
        self._collision_model = FileManager.get_collision_model()
        self._collision_model_len = len(self._collision_model)

    def set_bluetooth_trigger(self, enable):
        self._gyroBluetoothSendTrigger = enable

    def detect(self):
        sensor_data_store = []

        complementary_obj = {'x': 0}

        while True:
            acc_data = self._sensor.get_accel_data()
            gyro_data = self._sensor.get_gyro_data()

            if acc_data is None or gyro_data is None:
                print "none"
                continue

            absolute_acc = Calc.get_accel_vector(acc_data)
            complementary_obj = Calc.get_complementary(acc_data, gyro_data, complementary_obj)

            sensor_data_store.append(absolute_acc)

            if math.fabs(complementary_obj['x']) > PASS_ROLLOVER_AMOUNT or absolute_acc > PASS_ABSOULTE_ACC_AMOUNT:
                BluetoothRFCOMM.send_message(Signal.EMERGENCY + Signal.READ_BYTE_SEPARATE +
                                             str(absolute_acc) + Signal.READ_BYTE_SEPARATE +
                                             str(similarity) + Signal.READ_BYTE_SEPARATE +
                                             str(complementary_obj['x']))




    def run(self):
        t1 = threading.Thread(target=self.detect, args=())
        t1.daemon = True
        t1.start()

# END
