import requests
import json
import random
from multiprocessing import Process, Queue


request_url = "http://openapi.tuling123.com/openapi/api/v2"
api_key = "c83e8c03c71d43b6b0ce271d485896d8"
api_uid = "248138"


def main():
    while True:
        msg = input("MSG: \n").strip("\r\n ")
        if not msg:
            continue

        data = {
            "perception": {"inputText": {"text": msg}},
            "userInfo": {"apiKey": api_key, "userId": api_uid}
        }
        try:
            r = requests.post(url=request_url, data=json.dumps(data), timeout=3)
            r = json.loads(r.content, encoding="utf-8")
            intent = r.get("intent")
            if isinstance(r, dict) and 8008 < int(intent.get("code", 0)):
                r = r.get("results", [{}])[0].get("values", {}).get("text")
        except Exception:
            r = random.choice([
                "我的内心毫无波动，甚至开始智障……",
                "哎呀，你讲话太快了啦……",
                "emmmmmm……"
            ])

        print(r)


if __name__ == "__main__":
    main()
