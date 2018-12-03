from mpu6050 import mpu6050
import threading
import math
import time
import datetime
from velocity_corner import vel_corner

GYRO_ANGLE_DIVIDE = 131.
ACC_DIMENSION_DIVIDE=16384.
ANALYZE_INTERVAL_TIME = 5
ANGLE_DEVICE = 12
ACC_DEVICE = 1.5

#  DEFINE COMPLIMENTARY CONSTANTS
COMPLIMENTARY_ALPHA = 0.98
COMPLIMENTARY_DT = 0.02

# DEFINE BLUETOOTH
BT_SIGNAL_FILTER = "F"
BT_READ_BYTE_SEPARATE = "!S!"


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
        self._gyroData = {}
        self._gyroTrigger = False

    def set_bluetooth_trigger(self, enable):
        self._gyroTrigger = enable

    def detect(self, bluetooth_send_cb):
        vel_cor= vel_corner()
        time_interval = 0
        accel_interval = 0
        roll_interval = 0
        sensor_data_store = []

        angle_x = 0
        angle_y = 0

        while True:
            acc_data = self._sensor.get_accel_data()
            gyro_data = self._sensor.get_gyro_data()


            absolute_acc = math.sqrt(acc_data['x'] * acc_data['x'] +
                                     acc_data['y'] * acc_data['y'] +
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
            # self._gyroData['accel'] = absolute_acc

            cur_time = time.time()

            sensor_data_store.append({
                'time': time.time(),
                'accel': absolute_acc
            })
            accel_interval = accel_interval + absolute_acc

            remove_data = sensor_data_store[0]

            if cur_time - remove_data['time'] > ANALYZE_INTERVAL_TIME:
                accel_interval = accel_interval - remove_data['accel']

                store_size = len(sensor_data_store)
                accel_det = accel_interval / store_size
                self._gyroData['accel'] = accel_det

                sensor_data_store.remove(remove_data)
            if acc_data['z'] <= -ACC_DEVICE and vel_cor.get_running_state() is False:
                vel_cor.run(1)

            if (angle_x <= -ANGLE_DEVICE or angle_x >= ANGLE_DEVICE) and vel_cor.get_running_state() is False:
                vel_cor.run(2)


            if self._gyroTrigger is False:
                continue


            # bluetooth_send_cb(BT_SIGNAL_FILTER + BT_READ_BYTE_SEPARATE + (str)(self._gyroData['complimentary']) +
            #                 BT_READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) + BT_READ_BYTE_SEPARATE +
            #                 (str)(self._gyroData['accel']))
            bluetooth_send_cb(BT_SIGNAL_FILTER + BT_READ_BYTE_SEPARATE + (str)(self._gyroData['angle_x']) +
                              BT_READ_BYTE_SEPARATE + (str)(self._gyroData['accel']))

    def run(self, bluetooth_send_cb):
        t1 = threading.Thread(target=self.detect, args=(bluetooth_send_cb,))
        t1.daemon = True
        t1.start()

# END
