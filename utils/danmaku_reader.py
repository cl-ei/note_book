#!/usr/bin/env python3
import datetime
from redismq import RedisMessageQueue


BROWSER_DRIVER_PATH = "chromedriver.exe"
MONITOR_ADDR = "https://live.bilibili.com/612"


class DanmakuReader(object):
    def __init__(self, host):
        self.q = RedisMessageQueue(host=host, channel="chat")

    def run(self):
        print("Danmaku reader started.\n--------------------------\n")
        while True:
            raw_msgs = self.q.accept_msg()
            for raw_message in raw_msgs:
                try:
                    user, msg = raw_message.split("\n")[-1].split(" : ")
                    print("[%s]%s -> %s" % (str(datetime.datetime.now()), user, msg))
                except Exception as e:
                    print("Lost raw chat message. E: %s" % e)


if __name__ == "__main__":
    DanmakuReader("192.168.1.111").run()
