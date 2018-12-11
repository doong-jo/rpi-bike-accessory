import os
import matplotlib.pyplot as plt
import threading
from drawnow import *

SLEEPING_TIME = 1.0

class GraphDrawer(object):

    def __init__(self):
        self._loadValueArr = []

    def plotLoadAvg(self):
        plt.ylim(0, 4)
        plt.title('Raspberry Pi load average')
        plt.grid(True)
        plt.ylabel('usage')
        plt.plot(self._loadValueArr, 'bo-', label='usage')
        plt.legend(loc='upper right')

        for i in range(0, 100):
            self._loadValueArr.append(0)

    def draw(self, test_value):
        self.plotLoadAvg()

        while True:
            self._loadValueArr.append(test_value)
            self._loadValueArr.pop(0)
            drawnow(self.plotLoadAvg)
            plt.pause(1)

    def run(self, test_value):
        t1 = threading.Thread(target=self.draw, args=(test_value,))
        t1.daemon = True
        t1.start()
