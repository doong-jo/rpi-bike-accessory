from mpu6050 import mpu6050
import threading
import math
import time
import datetime
from velocity_corner import vel_corner

GYRO_ANGLE_DIVIDE = 131.
ACC_DIMENSION_DIVIDE=16384.
ANALYZE_INTERVAL_TIME = 3
ANGLE_DEVICE = 12
ACC_DEVICE = 1.5

#  DEFINE COMPLIMENTARY CONSTANTS
COMPLIMENTARY_ALPHA = 0.98
COMPLIMENTARY_DT = 0.02

# DEFINE BLUETOOTH
BT_SIGNAL_FILTER = "F"
BT_READ_BYTE_SEPARATE = "!S!"

COLLISTION_PATTERN = [
1.41226445188,
1.40029894184,
1.41644903838,
1.30749279495,
1.27942919918,
1.15871940068,
1.19272821459,
1.16987317898,
1.39911950112,
1.48676838746,
1.70403424208,
1.60415977962,
2.98468135234,
9.26755877997,
15.4548951434,
5.82454105117,
10.4481229521,
19.8617359319,
19.6431323521,
7.72910076886,
6.98685517678,
7.25668107286,
6.70277996069,
8.96742950234,
9.00531143954,
7.73123120373,
7.39294000715,
7.37609547121,
7.62725764654,
8.0206784758,
]

PATTERN_LENGTH = len(COLLISTION_PATTERN)

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
            'similarity': 0.0,
        }
        self._gyroTrigger = False

    def set_bluetooth_trigger(self, enable):
        self._gyroTrigger = enable

    def cosine_similarity(self, a, b):
        return sum([i * j for i, j in zip(a, b)]) / (
                    math.sqrt(sum([i * i for i in a])) * math.sqrt(sum([i * i for i in b])))

    def euclidean_distance(self, a, b):
        return math.sqrt(sum([(i - j) * (i - j) for i, j in zip(a, b)]))

    def get_coll_test_value(self):
        return self._gyroData['similarity']

    def detect(self, bluetooth_send_cb):
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

            self._gyroData['complimentary'] = dist(angle_x, angle_y)
            self._gyroData['angle_x'] = angle_x

            sensor_data_store.append(absolute_acc)

            if len(sensor_data_store) > PATTERN_LENGTH:
                sensor_data_store.pop(0)
                # print "cosigne_similarity : " + (str)(self.cosine_similarity(COLLISTION_PATTERN, sensor_data_store)) \
                #       + "/////" + (str)(absolute_acc)
                #

                self._gyroData['similarity'] = self.cosine_similarity(COLLISTION_PATTERN, sensor_data_store)
                # self._gyroData['similarity'] = self.euclidean_distance(COLLISTION_PATTERN, sensor_data_store)

                # if self.cosine_similarity(COLLISTION_PATTERN, sensor_data_store) > 0.9 :
                #     print "!!!!!!!!!!!!! Collision !!!!!!!!!!!!!!"

                # print "euclidean_distance : " + (str)(self.euclidean_distance(COLLISTION_PATTERN, sensor_data_store)) \
                #       + "/////" + (str)(absolute_acc)


            cur_time = time.time()

            # sensor_data_store.append({
            #     'time': time.time(),
            #     'accel': absolute_acc
            # })
            # accel_interval = accel_interval + absolute_acc
            #
            # remove_data = sensor_data_store[0]
            #
            # if cur_time - remove_data['time'] > ANALYZE_INTERVAL_TIME:
            #     accel_interval = accel_interval - remove_data['accel']
            #
            #     store_size = len(sensor_data_store)
            #     accel_det = accel_interval / store_size
            #     self._gyroData['accel'] = accel_det
            #
            #     sensor_data_store.remove(remove_data)




            # print (str)(datetime.datetime.now()) + " /////// " + (str)(absolute_acc)







            # slow-down and corner interface
            # if acc_data['z'] <= -ACC_DEVICE and vel_cor.get_running_state() is False:
            #     vel_cor.run(1)
            #
            # if (angle_x <= -ANGLE_DEVICE or angle_x >= ANGLE_DEVICE) and vel_cor.get_running_state() is False:
            #     vel_cor.run(2)

            if self._gyroTrigger is False:
                continue


            # bluetooth_send_cb(BT_SIGNAL_FILTER + BT_READ_BYTE_SEPARATE + (str)(self._gyroData['complimentary']) +
            #                 BT_READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) + BT_READ_BYTE_SEPARATE +
            #                 (str)(self._gyroData['accel']))


            #bluetooth_send_cb(BT_SIGNAL_FILTER + BT_READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) +
            #                  BT_READ_BYTE_SEPARATE + (str)(self._gyroData['accel']))

    def run(self, bluetooth_send_cb):
        t1 = threading.Thread(target=self.detect, args=(bluetooth_send_cb,))
        t1.daemon = True
        t1.start()

# END
