from gpiozero import MCP3008
import time
import threading



# DEFINE VALUE
ZERO_VALUE = 0.948
FULL_VALUE = 0.843
ARRAY_LENGTH = 60

# DEFINE BLUETOOTH
BT_SIGNAL_BAT = "BAT"
BT_READ_BYTE_SEPARATE = "!S!"

class State_of_Charge(object):

    def __init__(self):
        self.battery_array = []

        pass

    def setup(self):

        pot = MCP3008(0)
        return pot

    def battery_avg(self):

        avg_value = 0
        avg = 0
        for i in range(0, ARRAY_LENGTH):
            value = self.setup().value
            self.battery_array.insert(0, value)
            if len(self.battery_array) == ARRAY_LENGTH:
                for j in range(0, ARRAY_LENGTH):
                    avg_value = sum(self.battery_array)
                del self.battery_array[ARRAY_LENGTH - 1]
            avg = (avg_value / ARRAY_LENGTH)
        return avg

    def battery_indicator(self):
         while True:
            avg = self.battery_avg()
            print avg
            if avg < FULL_VALUE:
                soc = 'Charging'

            elif avg >= ZERO_VALUE:
                soc = '0%'
                print "it will be shutdown"

            else:
                soc = (str)(round((ZERO_VALUE - avg) * 100000 / 105)) + '%'

            print(soc)
            time.sleep(0.1)
            # bluetooth_send_cb(BT_SIGNAL_BAT + BT_READ_BYTE_SEPARATE + self.soc)

    def run(self):
        t1 = threading.Thread(target=self.battery_indicator)
        t1.daemon = True
        t1.start()

