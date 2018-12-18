from mpu6050 import mpu6050
import threading
import math
import datetime
from pytz import timezone
from bluetoothrfcomm import BluetoothRFCOMM
from velocity_corner import vel_corner
from filemgr import FileManager
from calc import *
from signal_interface import Signal
from buzer import Buzer

PASS_SIMIARITY_AMOUNT = 0.5
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
        vel_cor= vel_corner()
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

            if len(sensor_data_store) > self._collision_model_len:
                sensor_data_store.pop(0)

                similarity = Calc.cosine_similarity(self._collision_model, sensor_data_store)
                # print similarity

                if similarity > PASS_SIMIARITY_AMOUNT:
                    # print "!!!!!!!!!!!!! Pass accelerormeter !!!!!!!!!!!!!!"

                    # print math.fabs(complementary_obj['x'])
                    if math.fabs(complementary_obj['x']) > PASS_ROLLOVER_AMOUNT:
                        Buzer.start_sound(True)
                        # print "!!!!!!!!!!!!! Pass rollover !!!!!!!!!!!!!!"

                        BluetoothRFCOMM.send_message(Signal.EMERGENCY + Signal.READ_BYTE_SEPARATE +
                                                     str(absolute_acc) + Signal.READ_BYTE_SEPARATE +
                                                     str(similarity) + Signal.READ_BYTE_SEPARATE +
                                                     str(complementary_obj['x']))

                        self._gyroData['date'] = datetime.datetime.now(timezone('Asia/Seoul'))
                        self._gyroData['similarity'] = similarity
                        self._gyroData['accel'] = absolute_acc
                        self._gyroData['angle_x'] = complementary_obj['x']
                        FileManager.save_append_collision_log(self._gyroData)

                ##################### For write log ###################3
                # self._gyroData['date'] = datetime.datetime.now(timezone('Asia/Seoul'))
                # self._gyroData['accel'] = absolute_acc
                # self._gyroData['angle_x'] = complementary_obj['x']
                # FileManager.save_append_collision_log(self._gyroData)

            ################### slow-down and corner interface ###################
            # if acc_data['z'] <= -ACC_DEVICE and vel_cor.get_running_state() is False:
            #     vel_cor.run(1)
            #
            # if (angle_x <= -ANGLE_DEVICE or angle_x >= ANGLE_DEVICE) and vel_cor.get_running_state() is False:
            #     vel_cor.run(2)

            ######################### bluetooth #########################
            # if self._gyroBluetoothSendTrigger is False:
            #     continue

            # BluetoothRFCOMM.send_message(Signal.FILTER + Signal.READ_BYTE_SEPARATE + (str)(self._gyroData['complimentary']) +
            #                 Signal.READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) + Signal.READ_BYTE_SEPARATE +
            #                 (str)(self._gyroData['accel']))

            # BluetoothRFCOMM.send_message(Signal.FILTER + Signal.READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) +
            #                  Signal.READ_BYTE_SEPARATE + (str)(self._gyroData['accel']))

    def run(self):
        t1 = threading.Thread(target=self.detect, args=())
        t1.daemon = True
        t1.start()

# END
