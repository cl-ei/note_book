import redis
import pickle
import json

with open("redis_config.json") as f:
    REDIS_CONFIG = json.load(f)


class RedisMessageQueue(object):
    def __init__(self, channel=None):
        self.__conn = redis.Redis(**REDIS_CONFIG)
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
