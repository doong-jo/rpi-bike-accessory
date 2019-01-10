import time
import threading
from pattern_manager import PatternMgr
from pattern_interface import Pattern

#########CONSTATNT#####################
SLEEPING_TIME = 1.0
ACC_DEVICE = 5
ANGLE_DEVICE = 25
CLEARING_WAIT_TIME = 0.1
WAIT_TIME = 1.0
#########CONSTATNT#####################



class vel_corner(object):

    def __init__(self):

        pass

    def vel_cor(self, mpu):
        led_pattern = 0
        while True:
            if (PatternMgr.patternIdx != Pattern.BREAK_ON and
                PatternMgr.patternIdx != Pattern.SET_CLEAR):
                led_pattern = PatternMgr.patternIdx

            if mpu['acc_z'] <= -ACC_DEVICE or mpu['angle_x'] <= -ANGLE_DEVICE\
                    or mpu['angle_x'] >= ANGLE_DEVICE:
                PatternMgr.ledPhaseTrigger = False
                PatternMgr.set_pattern(Pattern.BREAK_ON)
                time.sleep(WAIT_TIME)
            else:
                PatternMgr.ledPhaseTrigger = True
                PatternMgr.set_pattern(led_pattern)
                time.sleep(0.03)
                # print led_pattern


    def run(self, mpu):
        t1 = threading.Thread(target=self.vel_cor, args=(mpu,))
        t1.daemon = True
        t1.start()