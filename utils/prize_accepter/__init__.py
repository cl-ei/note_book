#!/usr/bin/env python3
import re
import os
import time
import logging
from selenium import webdriver
from redismq import RedisMessageQueue
from exceptionsproc import IgnoreError


BROWSER_DRIVER_PATH = "./chromedriver.exe"
LOGIN_URL = "https://passport.bilibili.com/login"
LIVE_ADDR_PREFIX = "https://live.bilibili.com/"


class PrizeAccepter(object):
    def __init__(self, loger_name, log_file_path):
        self.browser = None
        self.original_window_handle = None
        self.redis_quene = RedisMessageQueue()

        logger = logging.getLogger(loger_name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(os.path.join("./", log_file_path), encoding="utf-8")
        fh.setFormatter(logging.Formatter("[%(asctime)s]%(message)s"))
        logger.addHandler(fh)
        self.prize_logging = logger

    def record_log_and_get_prize_cnt(self):
        prize_title = ""
        for _ in range(10):
            try:
                prize_title = self.browser.find_element_by_css_selector(".lottery-box .title").text
            except Exception:
                time.sleep(0.1)
            else:
                break
        if not prize_title:
            self.prize_logging.error("Cannot load title, url: %s" % self.browser.current_url)
            return 5

        thank_name = ""
        for _ in range(10):
            try:
                thank_name = self.browser.find_element_by_class_name("thx-name").text
            except Exception:
                time.sleep(0.1)
            else:
                break

        self.prize_logging.info("Prize title[%s][%s]" % (prize_title, thank_name))
        print("Got prize title: %s, provied by: %s" % (prize_title, thank_name))

        try:
            n = int([_ for _ in re.sub("\D", "-", prize_title).split("-") if _][-1])
        except Exception:
            n = 0

        if prize_title.find("小电视") > -1:
            prize_type = "TV"
        elif prize_title.find("花") > -1:
            prize_type = "FL"
        else:
            prize_type = "UN"

        print("prize: %s, count: %s." % (prize_type, n))
        self.prize_logging.info(
            "Accept prize[%s][%s][%s][%s]"
            % (self.browser.current_url, prize_type, n, thank_name)
        )
        return 5 if n < 1 else n + 10

    def accept_prize(self, room_number):
        url = LIVE_ADDR_PREFIX + room_number
        print("request url: ", url)
        self.browser.switch_to.window(self.original_window_handle)
        self.browser.execute_script("window.open('%s')" % url)

        for handle in [h for h in self.browser.window_handles if h != self.original_window_handle]:
            with IgnoreError(print_error=True):
                self.browser.switch_to.window(handle)

                # 等待页面加载完毕
                for _ in range(100):  # 0.1秒轮询一次，最多等待10秒
                    if not self.browser.find_elements_by_class_name("lottery-box"):
                        time.sleep(0.1)
                        continue

                    # 页面已经加载完毕，读取标题
                    prize_count = self.record_log_and_get_prize_cnt()

                    # 领奖
                    for _ in range(prize_count):
                        self.browser.execute_script('$(".lottery-box").trigger("click");')
                        time.sleep(0.05)
                    break
                else:
                    print("Page load faild!")
                    self.prize_logging.error("Fond prize url, but cannot load it: %s" % self.browser.current_url)

                self.browser.close()

    def run(self):
        print("Initialization...")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        self.browser = webdriver.Chrome(executable_path=BROWSER_DRIVER_PATH, port=9515, options=options)
        self.browser.get(LOGIN_URL)

        print("Starting...")
        input("Waiting for login...")
        print("Status ready.\n\n--------------------\n")

        self.original_window_handle = self.browser.current_window_handle
        while True:
            room_numbers = self.redis_quene.accept_msg()
            for r in room_numbers:
                self.accept_prize(r)
