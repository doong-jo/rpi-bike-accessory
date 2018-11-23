from mpu6050 import mpu6050
import threading
import time
import math

PI = 3.141592
SUM_COUNT = 3
EMERGENCY_ANGLE = 150
STOP_ANGLE = 30
ACCELEROMETER_SCALE=16384

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def dist(a,b):
    return math.sqrt((a*a)+(b*b))

class Gyroscope(object):

    def __init__(self):
        self.sensor = mpu6050(0x68)

    # def detect_emergency(self):
    #     for i in range(3):
    #         self.accel_calculate()




    def getAccelData(self):
        return self.gyroscope_sensor().accelerometer_data()

    def getGyroData(self):
        return self.gyroscope_sensor().get_gyro_data()


    def detect(self, inturruptLEDcb, bluetoothSendcb):
        angle_x = 0
        angle_y = 0
        i=0
        dgy_x_past=0
        dgy_y_past=0
        Total_Gap=0
        while True:
            Start_time=time.time()
            accel_data = self.sensor.get_accel_data()
            gyro_data = self.sensor.get_gyro_data()

            gyro_data_x = gyro_data['x'] / 131.
            gyro_data_y = gyro_data['y'] / 131.
            # gyro_data_z = gyro_data['z'] / 131.

            deg_x = get_x_rotation(accel_data['x'], accel_data['y'], accel_data['z'])
            deg_y = get_y_rotation(accel_data['x'], accel_data['y'], accel_data['z'])
            dgy_x = gyro_data_x
            dgy_y = gyro_data_y
            dgy_x_past = gyro_data_x
            dgy_y_past = gyro_data_y
            angle_x = (0.95 * (angle_x + (dgy_x * 0.004))) + (0.05 * deg_x)
            angle_y = (0.95 * (angle_y + (dgy_y * 0.004))) + (0.05 * deg_y)

            print("Complimentary Filtered degree data")
            print("Gyro_x: " + str(deg_x))
            print("Gyro_y: " + str(deg_y))
            print("angle_x: " + str(angle_x))
            print("angle_y " + str(angle_y))
            #
            # divAccel_X = accel_data['x'] / 16384.0
            # divAccel_Y = accel_data['y'] / 16384.0
            # divAccel_Z = accel_data['z'] / 16384.0
            #
            # rotation_X = get_x_rotation(divAccel_X, divAccel_Y, divAccel_Z)
            # rotation_Y = get_y_rotation(divAccel_X, divAccel_Y, divAccel_Z)

            Final_time = time.time()
            Gap_time=Final_time-Start_time
            i+=1
            Total_Gap+=Gap_time
            print("Avg Gap time"+str(Total_Gap/i))

            # self.accel_calculate()

    def run(self, inturruptLEDcb, bluetoothSendcb):
        t1 = threading.Thread(target=self.detect, args=(inturruptLEDcb, bluetoothSendcb,))
        t1.daemon = True
        t1.start()

# END

