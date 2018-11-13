from mpu6050 import mpu6050
import threading
import time
import math

PI = 3.141592
SUM_COUNT = 3
EMERGENCY_ANGLE = 150
STOP_ANGLE = 30

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
        while True:
            accel_data = self.sensor.get_accel_data()
            gyro_data = self.sensor.get_gyro_data()
            temp = self.sensor.get_temp()

            #print("Accelerometer data")
            #print("x: " + str(accel_data['x']))
            #print("y: " + str(accel_data['y']))
            #print("z: " + str(accel_data['z']))
            #
            #print("Gyroscope data")
            #print("x: " + str(gyro_data['x']))
            #print("y: " + str(gyro_data['y']))
            #print("z: " + str(gyro_data['z']))

            divAccel_X = accel_data['x'] / 16384.0
            divAccel_Y = accel_data['y'] / 16384.0
            divAccel_Z = accel_data['z'] / 16384.0

            rotation_X = get_x_rotation(divAccel_X, divAccel_Y, divAccel_Z)
            rotation_Y = get_y_rotation(divAccel_X, divAccel_Y, divAccel_Z)


            # print "X Rotation: ", get_x_rotation(divAccel_X, divAccel_Y,
            #                                      divAccel_Z)
            # print "Y Rotation: ", get_y_rotation(divAccel_X, divAccel_Y,
            #                                      divAccel_Z)

            IsEmergency = False

            angle_value = 0

            angle_value += gyro_data['x']
            angle_value += gyro_data['y']
            angle_value += gyro_data['z']
            
            print("angleX : " + str(gyro_data['x']));
            print("angleY : " + str(gyro_data['y']));
            print("angleZ : " + str(gyro_data['z']));

            print("angle_value : ")
            print math.fabs(angle_value)


            if math.fabs(angle_value) >= EMERGENCY_ANGLE:
                IsEmergency = True
                bluetoothSendcb("EMERGENCY")

            if math.fabs(gyro_data['y']) >= STOP_ANGLE:
                IsEmergency = True

            if rotation_X >= 20:
                inturruptLEDcb("left")
                print("inturrptLED RIGHT")
            elif rotation_X <= -20:
                inturruptLEDcb("right")
                print("inturrptLED LEFT")
            elif IsEmergency:
                inturruptLEDcb("emergency")
                print("inturrptLED EMNERGENCY")
            else:
                inturruptLEDcb("none")
                print("inturrptLED NONE")


            print("Temp: " + str(temp) + " C")
            # self.accel_calculate()
            time.sleep(0.25)

    # def accel_calculate(self) :
    #     accel_data = self.sensor.get_accel_data()
    #     gyro_data = self.sensor.get_gyro_data()
    #
    #     deg = math.atan2(accel_data['x'], accel_data['z']) * 180 /PI
    #     dgy_x = gyro_data['y'] / 131.
    #     self.angle = (0.95 * (self.angle + (dgy_x * 0.001))) + (0.5 * deg)
    #
    #     print("deg : " + deg)

    def run(self, inturruptLEDcb, bluetoothSendcb):
        t1 = threading.Thread(target=self.detect, args=(inturruptLEDcb, bluetoothSendcb,))
        t1.daemon = True
        t1.start()

# END

