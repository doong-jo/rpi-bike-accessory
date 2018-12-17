import RPi.GPIO as GPIO
import time
import threading

# ----------------DEFINE BUTTON ATTRIBUTE---------------- #

Cnt = 0
Pin_num = 18
Long_T = 2500
Short_T = 1000
# -------------------------------------------------------- #


class Button(object):
    def __init__(self):
        pass

    def Btn_setting(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        return 0

    def Time_cal(self):
        # Time calculating_Function
        RisingTime=time.time()
        a=GPIO.wait_for_edge(Pin_num, GPIO.RISING,timeout=Long_T)
        if Pin_num is a:
            Activated_Time = time.time()-RisingTime
        else:
            return Long_T
        return Activated_Time

    def Distinguising_push(self):
        Button.Btn_setting(self)

        while True:
            i = GPIO.wait_for_edge(Pin_num, GPIO.FALLING, timeout=Short_T)
            if i is Pin_num:
                Falling_Time=Button.Time_cal(self)
                if Falling_Time > Long_T/1000:
                    print("power on & off")
                elif Falling_Time < Short_T/1000:
                    Cnt+=1
                    if Cnt==3:
                        print("bluetooth on & off")
                        Cnt=0
                else:
                    Cnt=0
            else:
                Cnt = 0

    def run(self):

        t1 = threading.Thread(target=self.Distinguising_push)
        t1.daemon = True
        t1.start()