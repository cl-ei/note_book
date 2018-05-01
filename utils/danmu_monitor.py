#!/usr/bin/env python3
import re
import os
import time
import datetime
from selenium import webdriver
from redismq import RedisMessageQueue
from exceptionsproc import IgnoreError


BROWSER_DRIVER_PATH = "chromedriver.exe"
MONITOR_ADDR = "https://live.bilibili.com/612"


class DanmakuMonitor(object):
    def __init__(self):
        self.browser = None
        self.prize_redis_queue = RedisMessageQueue()
        self.chat_redis_queue = RedisMessageQueue(channel="chat")

        self.prize_logging = DanmakuMonitor.make_logger("prize_raw", "prize_raw.log")
        self.chat_logging = DanmakuMonitor.make_logger("chat", "chat.log")

    @staticmethod
    def make_logger(name, path):
        import logging
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(os.path.join("./", path), encoding="utf-8")
        fh.setFormatter(logging.Formatter("[%(asctime)s]%(message)s"))
        logger.addHandler(fh)
        return logger

    def clear_msg(self):
        while True:
            try:
                self.browser.find_element_by_class_name("icon-clear")
            except Exception:
                time.sleep(0.1)
            else:
                self.browser.execute_script('$(".icon-clear").trigger("click")')
                return

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

    def send_chat_danmaku_msg(self, chat_danmaku):
        if not chat_danmaku:
            return
        self.chat_redis_queue.send_msg(chat_danmaku)
        for raw_message in chat_danmaku:
            try:
                spilited_msg = [_ for _ in raw_message.split("\n") if _]
                if len(spilited_msg) == 2:
                    spilited_msg = ["", " " * 5] + spilited_msg
                user, msg = spilited_msg[-1].split(" : ")
                honor = "%s" % (spilited_msg[0] + spilited_msg[1])
                ul = "%-5s" % spilited_msg[2]
                time_str = str(datetime.datetime.now())[:-3]
                message = "[%s][%s] %s -> %s" % (ul, honor, user, msg,)
                print("[%s]%s" % (time_str, message))
                self.chat_logging.info(message)
            except Exception as e:
                print("Lost raw chat message. E: %s" % e)

    def send_prize_danmaku_msg(self, prize_danmaku):
        if not prize_danmaku:
            return

        room_list = []
        for raw_msg in prize_danmaku:
            with IgnoreError():
                valid_room_numbers = [
                    _ for _ in re.sub("\D", "-", raw_msg).split("-")
                    if _ and 10 > len(_) > 2
                ]
                if valid_room_numbers:
                    self.prize_logging.info("Prize raw msg[%s]" % raw_msg)
                room_list.extend(valid_room_numbers)
                print("Prize raw msg -> ", raw_msg.replace("\r", "\\r").replace("\n", "\\n"))
        self.prize_redis_queue.send_msg(list(set(room_list)))

    def send_heart_beat(self):
        heart_beat_danmaku = ["HEART BEAT!"]
        self.chat_redis_queue.send_msg(heart_beat_danmaku)
        self.prize_redis_queue.send_msg(heart_beat_danmaku)
        print("[%s]Heart beat message sent." % (str(datetime.datetime.now())[:-3]))

    def run(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--mute-audio")

        self.browser = webdriver.Chrome(executable_path=BROWSER_DRIVER_PATH, port=9515, options=options)
        self.browser.get(MONITOR_ADDR)
        self.clear_msg()

        print("Message monitor started! ")
        print("Status ready.\n\n--------------------\n")

        idle_time = 0
        while True:
            prize_danmaku = self.parse_prize_danmaku()
            chat_danmaku = self.parse_chat_danmaku()

            if prize_danmaku or chat_danmaku:
                self.clear_msg()
                self.send_prize_danmaku_msg(prize_danmaku)
                self.send_chat_danmaku_msg(chat_danmaku)
                idle_time = 0
            else:
                time.sleep(2)
                idle_time += 2

            if idle_time >= 60:
                idle_time = 0
                self.send_heart_beat()


if __name__ == "__main__":
    DanmakuMonitor().run()
