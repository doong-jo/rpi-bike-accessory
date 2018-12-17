import threading


class Battery(object):
    def __init__(self):
        pass

    def indicate(self):
        pass

    def run(self):
        t1 = threading.Thread(target=self.indicate)
        t1.daemon = True
        t1.start()
