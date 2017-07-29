import requests
import json
import time


def get_my_ip():
    try:
        r = requests.get(url='http://ip.taobao.com/service/getIpInfo2.php', params={"ip": "myip"}, timeout=5)
    except Exception as e:
        return None
    try:
        data = json.loads(r.text)
        return data.get("data", {}).get("ip")
    except:
        return None


def load_my_ip():
    with open("./my_ip.txt", "r+") as f:
        return f.read()


def save_my_ip(data):
    with open("./my_ip.txt", "w") as f:
        f.write(data)
    return True


def init_url_map():
    for _ in range(3):
        my_ip = get_my_ip()
        if my_ip:
            break
        else:
            time.sleep(5)
    else:
        raise ValueError("Cannot get my ip!")

    saved_ip = load_my_ip()
    save_my_ip(my_ip)
    return my_ip != saved_ip


print init_url_map()
