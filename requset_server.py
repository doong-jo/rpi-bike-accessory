import threading
import datetime
import requests
import time

# DEFINE POST REQUEST
URL = "http://175.123.140.145/"
DEVICE_COLLECTION = "devicetest"


def convert_object_to_string(targetQuery):
    resultQueryStr = '?'

    objectLen = len(targetQuery)

    cnt = 0
    for key in targetQuery:
        value = targetQuery[key]

        resultQueryStr = resultQueryStr + key + '=' + (str)(value)
        if cnt + 1 != objectLen:
            resultQueryStr += '&'
        cnt += 1

    return resultQueryStr


class RequestMgr(object):

    def __init__(self):
        pass

    def request(self, gyroData):

        while True:
            now = datetime.datetime.now()

            dateObj = {
                'year': (str)(now.year),
                'month': (str)(now.month),
                'day': (str)(now.day),
                'hour': (str)(now.hour + 19),
                'minute': (str)(now.minute),
                'second': (str)(now.second),
            }
            for key in dateObj:
                if len(dateObj[key]) == 1:
                    dateObj[key] = '0' + dateObj[key]


            resultDate = "%(year)s-%(month)s-%(day)sT%(hour)s:%(minute)s:%(second)s" % dateObj

            queryObj = {}
            queryObj['device_name'] = 'EIGHT_1001'
            queryObj['complimentary'] = gyroData['complimentary']
            queryObj['roll'] = gyroData['angle_x']
            queryObj['occured_date'] = resultDate

            endPoint = URL + DEVICE_COLLECTION + convert_object_to_string(queryObj)

            requests.post(endPoint, data={})

    def run(self, gyroData):
        t1 = threading.Thread(target=self.request, args=(gyroData,))
        t1.daemon = True
        t1.start()

# END
