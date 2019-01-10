from mpu6050 import mpu6050
import threading
from calc import *
from pattern_manager import PatternMgr

THR_ROLLOVER_AMOUNT = 25
THE_ACC_AMOUNT = 10


class Mpu(object):
    inturrptGyro = False

    def __init__(self):
        self._sensor = mpu6050(0x68)
        self._gyroData = {
            'date': '',
            'accel': 0.0,
            'angle_x': 0.0,
        }
        self._gyroBluetoothSendTrigger = False

    def set_bluetooth_trigger(self, enable):
        self._gyroBluetoothSendTrigger = enable

    def detect(self):
        complementary_obj = {'x': 0}
        acc_data = {}
        gyro_data = {}

        while True:
            acc_data = self._sensor.get_accel_data()
            gyro_data = self._sensor.get_gyro_data()

            if acc_data is None or gyro_data is None:
                continue

            try:
                absolute_acc = Calc.get_accel_vector(acc_data)
                complementary_obj = Calc.get_complementary(acc_data, gyro_data, complementary_obj)

            except AttributeError:
                continue

            if acc_data['z'] <= -THE_ACC_AMOUNT or \
                    complementary_obj['x'] <= -THR_ROLLOVER_AMOUNT\
                    or complementary_obj['x'] >= THR_ROLLOVER_AMOUNT:
                Mpu.inturrptGyro = True
                PatternMgr.set_break_trigger(True)

            else:
                Mpu.inturrptGyro = False
                PatternMgr.set_break_trigger(False)

    @staticmethod
    def get_inturrptGyro():
        return Mpu.inturrptGyro

    def run(self):
        t1 = threading.Thread(target=self.detect, args=())
        t1.daemon = True
        t1.start()

# END