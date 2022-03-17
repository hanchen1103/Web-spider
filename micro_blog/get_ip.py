import json
import logging
import random
import threading
import time
from threading import Thread

import redis
import requests
import urllib3

from micro_blog.config import bin_ip_url, proxy_cloucd_headers, get_ip_url, proxy_url, ip_proxy_list_key, dragonfly_ip

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

rds = redis.StrictRedis(host='127.0.0.1', port=6379, db=3, decode_responses=True)


def get_ip_proxies(count):
    ip_url = str.format(get_ip_url, count)
    return requests.get(ip_url, headers=proxy_cloucd_headers).text.split(":57114\r\n")


def verify_ip_useful(ip):
    if not ip or ip == '':
        return False
    try:
        response = requests.get(bin_ip_url, headers=proxy_cloucd_headers,
                                proxies={'http': 'http://' + ip, 'https': 'https://' + ip}).json()
    except requests.ConnectionError and json.decoder.JSONDecodeError as ex:
        logging.error(ex)
        return False
    logging.info("ip: " + ip + " approved")
    rds.lpush(ip_proxy_list_key, ip)
    rds.setex(ip, 1 * 60, '1')
    return ip.split(":")[0] == response.get('origin')


def rm_ip(ip):
    rds.lrem(ip_proxy_list_key, 1, ip)
    rds.delete(ip)


def request_ip():
    ip = get_ip_proxies(150)
    ip_pool = []
    for i in ip:
        verify_ip_useful(i)
    return ip_pool


def get_ip():
    ip_list = rds.zrangebyscore(ip_proxy_list_key, 0, int(time.time() - 120))
    if not ip_list or len(ip_list) == 0:
        return '127.0.0.1:1087'
    logging.info(ip_list)
    return random.choice(ip_list)


def get_response(url, headers, retry_count=6):
    logging.info("retry times is:" + str(-1 * (retry_count - 6)))
    if retry_count == 0:
        return
    try:
        ip_proxy = get_ip_proxy()
        logging.info("request {} ip address is: {}".format(url, str(ip_proxy)))
        response = requests.get(url, headers=headers, proxies=ip_proxy, verify=False)
        if response.status_code == 200:
            return response
        get_response(url, headers, retry_count - 1)
    except requests.ConnectionError and requests.exceptions.ConnectTimeout and requests.exceptions.ReadTimeout and \
           urllib3.exceptions.ConnectTimeoutError and requests.exceptions.ProxyError as e:
        logging.error(e)
        get_response(url, headers, retry_count - 1)

def get_ip_proxy():
    ip = get_ip()
    return {
        'http': 'http://' + ip,
        'https': 'https://' + ip,
    }


def get_dragonfly_ip():
    response = requests.get(dragonfly_ip, headers=proxy_cloucd_headers, timeout=3).json()
    if response:
        data_list = response.get("data")
        for i in data_list:
            ip = i.get("host") + ':' + i.get("port")
            logging.info(ip)
            # verify_ip_useful(ip)
            rds.zadd(ip_proxy_list_key, {ip: int(time.time())})


class replenish_ip_pool(threading.Thread):

    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        while True:
            if rds.zcard(ip_proxy_list_key) < 100:
                logging.info("time to get ip")
                get_dragonfly_ip()
                time.sleep(15)


class clear_invaild_ip(threading.Thread):

    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        while True:
            list = rds.zrangebyscore(ip_proxy_list_key, -10000000000, 10000000000)
            if len(list) < 30:
                time.sleep(1)
            for i in list:
                if int(rds.zscore(ip_proxy_list_key, i)) + 120 < int(time.time()):
                    rds.zrem(ip_proxy_list_key, i)
                    logging.info("delete invaild ip is:" + i)
            time.sleep(30)


# async def main():
#     L = await asyncio.gather(
#         replenish_ip_pool(),
#         clear_invaild_ip(),
#     )
#     print(L)


if __name__ == "__main__":
    thread1 = clear_invaild_ip(1, "Thread-1", 1)
    thread2 = replenish_ip_pool(2, "Thread-2", 2)
    thread2.start()
    thread1.start()
