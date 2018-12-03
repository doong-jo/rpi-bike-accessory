import time
import threading

SLEEPING_TIME = 1.0

class vel_corner(object):

    def __init__(self):
        self._isRunning = False
        pass

    def vel_cor(self, state):
        self._isRunning = True
        if state == 1:
            print('**********************************************************************8')
            time.sleep(SLEEPING_TIME)
        if state == 2:
            print 'tilted'
            time.sleep(SLEEPING_TIME)
        self._isRunning = False

    def get_running_state(self):
        return self._isRunning

    def run(self, velocity):
        t1 = threading.Thread(target=self.vel_cor, args=(velocity,))
        t1.daemon = True
        t1.start()
