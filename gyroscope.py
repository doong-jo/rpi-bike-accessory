from mpu6050 import mpu6050
import threading
import math
import time

GYRO_ANGLE_DIVIDE = 131.

#  DEFINE COMPLIMENTARY CONSTANTS
COMPLIMENTARY_ALPHA = 0.95
COMPLIMENTARY_DT = 0.03

# DEFINE BLUETOOTH
BT_SIGNAL_FILTER = "F"
BT_READ_BYTE_SEPARATE = "!S!"

# DEFINE POST REQUEST
URL = "http://175.123.140.145/"
DEVICE_COLLECTION = "devicetest"

def get_y_rotation(x, y, z):
    radians = math.atan2((-1)*z, dist(y, x))
    return -math.degrees(radians)


def get_z_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def dist(a, b):
    return math.sqrt((a*a)+(b*b))


class Gyroscope(object):

    def __init__(self):
        self.sensor = mpu6050(0x68)
        self.gyroData = {}

    def detect(self, inturruptLEDcb, bluetoothSendcb):
        angle_x = 0
        angle_y = 0

        while True:
            accel_data = self.sensor.get_accel_data()
            gyro_data = self.sensor.get_gyro_data()

            gyro_data_z = -1* gyro_data['z'] / GYRO_ANGLE_DIVIDE
            gyro_data_y = gyro_data['y'] / GYRO_ANGLE_DIVIDE
            deg_x = get_z_rotation(accel_data['x'], accel_data['y'], accel_data['z'])
            deg_y = get_y_rotation(accel_data['x'], accel_data['y'], accel_data['z'])
            dgy_z = gyro_data_z
            dgy_y = gyro_data_y
            angle_x = (COMPLIMENTARY_ALPHA * (angle_x + (dgy_z * COMPLIMENTARY_DT))) + ((1-COMPLIMENTARY_ALPHA) * deg_x)
            angle_y = (COMPLIMENTARY_ALPHA * (angle_y + (dgy_y * COMPLIMENTARY_DT))) + ((1-COMPLIMENTARY_ALPHA) * deg_y)

            self.gyroData['complimentary'] = dist(angle_x, angle_y)
            self.gyroData['angle_x'] = angle_x

            print("Complimentary Filtered degree data")
            print("Gyro_x: " + str(deg_x))
            print("Gyro_y: " + str(deg_y))
            print("angle_x: " + str(angle_x))
            print("angle_y " + str(angle_y))

            bluetoothSendcb(BT_SIGNAL_FILTER + BT_READ_BYTE_SEPARATE + (str)(self.gyroData['complimentary']) +
                            BT_READ_BYTE_SEPARATE + (str)(self.gyroData['angle_x']))


    def run(self, inturruptLEDcb, bluetoothSendcb):
        t1 = threading.Thread(target=self.detect, args=(inturruptLEDcb, bluetoothSendcb,))
        t1.daemon = True
        t1.start()

# END
