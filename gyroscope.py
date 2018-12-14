from mpu6050 import mpu6050
import threading
import math
import datetime
from pytz import timezone
from velocity_corner import vel_corner
from filemgr import FileManager

GYRO_ANGLE_DIVIDE = 131.
ACC_DIMENSION_DIVIDE=16384.
ANALYZE_INTERVAL_TIME = 3
RESPONSE_ANGLE_LED = 12
RESPONSE_ACC_DEVICE = 1.5

#  DEFINE COMPLIMENTARY CONSTANTS
COMPLIMENTARY_ALPHA = 0.98
COMPLIMENTARY_DT = 0.02

# DEFINE BLUETOOTH
BT_SIGNAL_FILTER = "F"
BT_READ_BYTE_SEPARATE = "!S!"

PATTERN_SAMPLE = {}
PATTERN_LENGTH = 50

def get_y_rotation(x, y, z):
    radians = math.atan2((-1)*z, dist(y, x))
    return -math.degrees(radians)


def get_z_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def dist(a, b):
    return math.sqrt((a*a)+(b*b))


class Mpu(object):

    def __init__(self):
        self._sensor = mpu6050(0x68)
        self._gyroData = {
            'complimentary': 0.0,
            'angle_x': 0.0,
        }
        self._gyroBluetoothSendTrigger = False
        self._collision_model = FileManager.get_collision_model()
        self._collision_model_len = len(self._collision_model)

    def set_bluetooth_trigger(self, enable):
        self._gyroBluetoothSendTrigger = enable

    def cosine_similarity(self, a, b):
        return sum([i * j for i, j in zip(a, b)]) / (
                    math.sqrt(sum([i * i for i in a])) * math.sqrt(sum([i * i for i in b])))

    def euclidean_distance(self, a, b):
        return math.sqrt(sum([(i - j) * (i - j) for i, j in zip(a, b)]))

    def detect(self, bluetooth_send_cb, buzer_sound):
        vel_cor= vel_corner()
        sensor_data_store = []

        angle_x = 0
        angle_y = 0

        while True:
            acc_data = self._sensor.get_accel_data()
            gyro_data = self._sensor.get_gyro_data()

            # except x-axis (gravity)
            absolute_acc = math.sqrt(acc_data['y'] * acc_data['y'] +
                                     acc_data['z'] * acc_data['z'])

            gyro_data_z = -1 * gyro_data['z'] / GYRO_ANGLE_DIVIDE
            gyro_data_y = gyro_data['y'] / GYRO_ANGLE_DIVIDE
            deg_x = get_z_rotation(acc_data['x'], acc_data['y'], acc_data['z'])
            deg_y = get_y_rotation(acc_data['x'], acc_data['y'], acc_data['z'])
            dgy_z = gyro_data_z
            dgy_y = gyro_data_y
            angle_x = (COMPLIMENTARY_ALPHA * (angle_x + (dgy_z * COMPLIMENTARY_DT))) + ((1-COMPLIMENTARY_ALPHA) * deg_x)
            angle_y = (COMPLIMENTARY_ALPHA * (angle_y + (dgy_y * COMPLIMENTARY_DT))) + ((1-COMPLIMENTARY_ALPHA) * deg_y)

            # self._gyroData['complimentary'] = dist(angle_x, angle_y)

            sensor_data_store.append(absolute_acc)

            if len(sensor_data_store) > self._collision_model_len:
                sensor_data_store.pop(0)

                self._gyroData['date'] = datetime.datetime.now(timezone('Asia/Seoul'))
                self._gyroData['accel'] = absolute_acc
                self._gyroData['angle_x'] = angle_x

                FileManager.save_append_collision_log(self._gyroData)

                if self.cosine_similarity(self._collision_model, sensor_data_store) > 0.9:
                    buzer_sound(True)
                    print self._gyroData['angle_x']
                    print "!!!!!!!!!!!!! Collision !!!!!!!!!!!!!!"


            # slow-down and corner interface
            # if acc_data['z'] <= -ACC_DEVICE and vel_cor.get_running_state() is False:
            #     vel_cor.run(1)
            #
            # if (angle_x <= -ANGLE_DEVICE or angle_x >= ANGLE_DEVICE) and vel_cor.get_running_state() is False:
            #     vel_cor.run(2)

            if self._gyroBluetoothSendTrigger is False:
                continue

            # bluetooth_send_cb(BT_SIGNAL_FILTER + BT_READ_BYTE_SEPARATE + (str)(self._gyroData['complimentary']) +
            #                 BT_READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) + BT_READ_BYTE_SEPARATE +
            #                 (str)(self._gyroData['accel']))


            #bluetooth_send_cb(BT_SIGNAL_FILTER + BT_READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) +
            #                  BT_READ_BYTE_SEPARATE + (str)(self._gyroData['accel']))

    def run(self, bluetooth_send_cb, buzer_sound):
        t1 = threading.Thread(target=self.detect, args=(bluetooth_send_cb, buzer_sound,))
        t1.daemon = True
        t1.start()

# END
