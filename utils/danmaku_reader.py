#!/usr/bin/env python3
import datetime
from redismq import RedisMessageQueue


BROWSER_DRIVER_PATH = "chromedriver.exe"
MONITOR_ADDR = "https://live.bilibili.com/612"


class DanmakuReader(object):
    def __init__(self):
        self.q = RedisMessageQueue(channel="chat")

    def run(self):
        print("Danmaku reader started.\n--------------------------\n")
        while True:
            raw_msgs = self.q.accept_msg()
            for raw_message in raw_msgs:
                time_str = str(datetime.datetime.now())[:-3]
                try:
                    spilited_msg = [_ for _ in raw_message.split("\n") if _]
                    if len(spilited_msg) == 2:
                        spilited_msg = ["", " " * 5] + spilited_msg
                    user, msg = spilited_msg[-1].split(" : ")
                    honor = "%s" % (spilited_msg[0] + spilited_msg[1])
                    ul = "%-5s" % spilited_msg[2]
                    message = "[%s][%s] %s -> %s" % (ul, honor, user, msg,)
                    print("[%s]%s" % (time_str, message))
                except Exception as e:
                    print(
                        "[%s]Lost raw chat message. E: %s" % (time_str, e),
                        "\n------------\n",
                        raw_message,
                        "\n------------"
                    )


if __name__ == "__main__":
    DanmakuReader().run()
