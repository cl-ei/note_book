#!/usr/bin/env python3
import re
import os
import time
from selenium import webdriver
from redismq import RedisMessageQueue
from exceptionsproc import IgnoreError


BROWSER_DRIVER_PATH = "chromedriver.exe"
MONITOR_ADDR = "https://live.bilibili.com/612"


def __make_logger(name, file_path, debug_format=False):
    import logging

    fh = logging.FileHandler(os.path.join("./", file_path), encoding="utf-8")
    if debug_format:
        log_format = "%(levelname)s %(asctime)s %(filename)s:%(lineno)d:%(funcName)s %(message)s"
    else:
        log_format = "[%(asctime)s]%(message)s"
    fh.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger


prize_logging = __make_logger(name="prize", file_path="prize_raw.log")


class DanmakuMonitor(object):
    def __init__(self):
        self.browser = None
        self.prize_redis_queue = RedisMessageQueue()
        self.chat_redis_queue = RedisMessageQueue(channel="chat")

    def clear_msg(self):
        while True:
            try:
                self.browser.find_element_by_class_name("icon-clear")
            except Exception:
                time.sleep(0.1)
            else:
                self.browser.execute_script('$(".icon-clear").trigger("click")')
                return

    @staticmethod
    def get_datetime_str():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def parse_prize_danmaku(self):
        prize_danmaku = []
        for m in self.browser.find_elements_by_class_name("system-msg"):
            with IgnoreError():
                prize_danmaku.append(m.text)
        return prize_danmaku

    def parse_chat_danmaku(self):
        chat_danmaku = []
        for m in self.browser.find_elements_by_class_name("danmaku-item"):
            with IgnoreError():
                chat_danmaku.append(m.text)
        return chat_danmaku

    def run(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        self.browser = webdriver.Chrome(executable_path=BROWSER_DRIVER_PATH, port=9515, options=options)
        self.browser.get(MONITOR_ADDR)
        self.clear_msg()

        print("Message monitor started! ")
        print("Status ready.\n\n--------------------\n")
        while True:
            # 获取领奖房间号
            prize_danmaku = self.parse_prize_danmaku()
            chat_danmaku = self.parse_chat_danmaku()

            if prize_danmaku or chat_danmaku:
                self.clear_msg()
            else:
                time.sleep(2)

            if prize_danmaku:
                room_list = []
                for raw_msg in prize_danmaku:
                    with IgnoreError():
                        valid_room_numbers = [
                            _ for _ in re.sub("\D", "-", raw_msg).split("-")
                            if _ and 10 > len(_) > 2
                        ]
                        if valid_room_numbers:
                            prize_logging.info("Prize raw msg[%s]" % raw_msg)
                        room_list.extend(valid_room_numbers)
                self.prize_redis_queue.send_msg(list(set(room_list)))

            if chat_danmaku:
                self.chat_redis_queue.send_msg(chat_danmaku)
                for raw_message in chat_danmaku:
                    try:
                        user, msg = raw_message.split("\n")[-1].split(" : ")
                        message = "[%s]%s -> %s" % (self.get_datetime_str(), user, msg)
                        print(message)
                    except Exception as e:
                        print("Lost raw chat message. E: %s" % e)


if __name__ == "__main__":
    DanmakuMonitor().run()
