from mpu6050 import mpu6050
import threading
import time
import math

GYRO_ANGLE_DIVIDE = 131.

#  DEFINE COMPLIMENTARY CONSTANTS
COMPLIMENTARY_ALPHA = 0.95
COMPLIMENTARY_DT = 0.03


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def dist(a, b):
    return math.sqrt((a*a)+(b*b))


class Gyroscope(object):

    def __init__(self):
        self.sensor = mpu6050(0x68)

    def detect(self, inturruptLEDcb, bluetoothSendcb):
        angle_x = 0
        angle_y = 0

        while True:
            accel_data = self.sensor.get_accel_data()
            gyro_data = self.sensor.get_gyro_data()

            gyro_data_x = gyro_data['x'] / GYRO_ANGLE_DIVIDE
            gyro_data_y = gyro_data['y'] / GYRO_ANGLE_DIVIDE

            deg_x = get_x_rotation(accel_data['x'], accel_data['y'], accel_data['z'])
            deg_y = get_y_rotation(accel_data['x'], accel_data['y'], accel_data['z'])
            dgy_x = gyro_data_x
            dgy_y = gyro_data_y
            angle_x = (COMPLIMENTARY_ALPHA * (angle_x + (dgy_x * COMPLIMENTARY_DT))) + ((1-COMPLIMENTARY_ALPHA) * deg_x)
            angle_y = (COMPLIMENTARY_ALPHA * (angle_y + (dgy_y * COMPLIMENTARY_DT))) + ((1-COMPLIMENTARY_ALPHA) * deg_y)

            print("Complimentary Filtered degree data")
            print("Gyro_x: " + str(deg_x))
            print("Gyro_y: " + str(deg_y))
            print("angle_x: " + str(angle_x))
            print("angle_y " + str(angle_y))

    def run(self, inturruptLEDcb, bluetoothSendcb):
        t1 = threading.Thread(target=self.detect, args=(inturruptLEDcb, bluetoothSendcb,))
        t1.daemon = True
        t1.start()

# END

