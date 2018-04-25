#!/usr/bin/env python
import sys
import paramiko
import time
import json
import logging
import traceback
import StringIO

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

reload(sys)
sys.setdefaultencoding('utf-8')

LOG_PATH = "/root/dynamic_ip_opeartion/"
logger = logging.getLogger('dynamic_ip')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_PATH + 'dynamic_ip.log')
formatter = logging.Formatter('%(levelname)s %(asctime)s %(funcName)s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


config_file = "/etc/clconfig/dynamic_ip_config.json"
with open(config_file) as config_file:
    config = json.load(config_file)


router_config = config.get("router")
HOSTNAME = router_config.get("HOSTNAME")
PORT = router_config.get("PORT")
USERNAME = router_config.get("USERNAME")
PASSWORD = router_config.get("PASSWORD")

aliyun_config = config.get("aliyun")
AccessKeyId = aliyun_config.get("AccessKeyId").encode("utf-8")
AccessKeySecret = aliyun_config.get("AccessKeySecret").encode("utf-8")
RegionId = aliyun_config.get("RegionId").encode("utf-8")

domain_config = config.get("domain")


def save_error_info():
    except_trace = StringIO.StringIO()
    traceback.print_exc(file=except_trace)
    logging.error('Error: %s' % except_trace.getvalue())
    except_trace.close()


def modify_record(my_ip):
    acs_client = AcsClient(AccessKeyId, AccessKeySecret, RegionId)
    for domain in domain_config:
        recored_id = domain.get("recored_id")
        prefix = domain.get("prefix").encode("utf-8")
        logging.info("Now set recored_id: %s, prefix: %s -> %s" % (recored_id, prefix, my_ip))

        request = UpdateDomainRecordRequest()
        request.set_RecordId(recored_id)
        request.set_RR(prefix)
        request.set_Type("A")
        request.set_Value(my_ip)
        request.set_TTL(600)
        try:
            response = acs_client.do_action_with_exception(request)
        except Exception as e:
            logger.error("Sync to aliyun error: %s." % e)
            save_error_info()
        else:
            logger.info("Sync to aliyun finished, nore info: %s" % response)


def load_ip():
    with open("/root/dynamic_ip_opeartion/ip") as f:
        return f.read()


def save_ip(ip):
    with open("/root/dynamic_ip_opeartion/ip", "w") as f:
        f.write(ip)
    return True


def ip_monitor():
    my_ip = load_ip()

    global client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=HOSTNAME,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        timeout=5
    )
    runtime_count = 0
    while True:
        runtime_count += 1
        if runtime_count >= 100:
            logger.info("Just recored hart beat. current ip: %s" % my_ip)
            runtime_count = 0

        time.sleep(5)
        stdin, stdout, stderr = client.exec_command('ifconfig ppp0 | grep "inet addr"')
        inet_info = stdout.read().strip()
        ip_addr = inet_info.split(" ")[1].split(":")[1]
        if ip_addr != my_ip:
            save_ip(ip_addr)
            my_ip = ip_addr

            logger.info("Ip changed: [%s], now sync to aliyun." % my_ip)
            modify_record(ip_addr)


def close_ssh_client(cli):
    if isinstance(cli, paramiko.SSHClient):
        try:
            cli.close()
        except:
            save_error_info()
            pass
    return True


if __name__ == '__main__':
    time.sleep(60)
    logger.info("Start proc.")
    client = None
    while True:
        try:
            ip_monitor()
        except Exception as error:
            logger.error("Error happend: %s. retry now ..." % error)
            save_error_info()

            close_ssh_client(client)
            client = None
            time.sleep(5)
