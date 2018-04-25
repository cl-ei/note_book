#!/usr/bin/env python3
import re
import os
import time
import logging
import redis
import pickle
from selenium import webdriver


BROWSER_DRIVER_PATH = "chromedriver.exe"
LOGIN_URL = "https://passport.bilibili.com/login"
LIVE_ADDR_PREFIX = "https://live.bilibili.com/"
LOG_FILE_PATH = "prize.log"


logger = logging.getLogger("prize")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join("./", LOG_FILE_PATH), encoding="utf-8")
fh.setFormatter(logging.Formatter("[%(asctime)s]%(message)s"))
logger.addHandler(fh)
prize_logging = logger


class RedisMessageQueue(object):
    def __init__(self, channel=None, **config):
        self.__conn = redis.Redis(
            host=config.get("host", "localhost"),
            port=config.get("port", 6379),
            db=config.get("db", 8),
        )
        self.channel = channel or "async"
        self._monitor_q = None

    def send_msg(self, msg):
        b = pickle.dumps(msg)
        self.__conn.publish(self.channel, b)
        return True

    def __init_monitor_q(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.listen()
        pub.parse_response()
        self._monitor_q = pub

    def accept_msg(self):
        if self._monitor_q is None:
            self.__init_monitor_q()
        while True:
            r = self._monitor_q.parse_response()
            try:
                return pickle.loads(r[-1])
            except Exception:
                continue


class IgnoreError(object):
    def __init__(self, print_error=False):
        self.__print_error = print_error

    def __enter__(self, *args):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and self.__print_error:
            print("An error happend! e: %s" % exc_type)
        return True


class PrizeAccepter(object):
    def __init__(self):
        self.browser = None
        self.original_window_handle = None
        self.redis_quene = RedisMessageQueue()

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
            prize_logging.error("Cannot load title, url: %s" % self.browser.current_url)
            return 5

        thank_name = ""
        for _ in range(10):
            try:
                thank_name = self.browser.find_element_by_class_name("thx-name").text
            except Exception:
                time.sleep(0.1)
            else:
                break

        prize_logging.info("Prize title[%s][%s]" % (prize_title, thank_name))
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
        prize_logging.info(
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
                    logging.error("Fond prize url, but cannot load it: %s" % browser.current_url)

                self.browser.close()

    def run(self):
        print("Initialization...")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        self.browser = webdriver.Chrome(executable_path=BROWSER_DRIVER_PATH, port=9515, options=options)
        self.browser.get(LOGIN_URL)

        print("Starting...")
        input("Waiting for login...")
        print("Status ready.\n\n--------------------\n")

        self.original_window_handle = self.browser.current_window_handle
        while True:
            room_numbers = self.redis_quene.accept_msg()
            print(room_numbers)
            for r in room_numbers:
                print("received: ", r)
                # self.accept_prize(r)


if __name__ == "__main__":
    PrizeAccepter().run()
