import json
import logging
import random
import time

import requests

from micro_blog.config import bin_ip_url, proxy_cloucd_headers, get_ip_url, proxy_url, ip_proxy_list_key
from micro_blog.explain_url import rds

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_ip_proxies(count):
    ip_url = str.format(get_ip_url, count)
    return requests.get(ip_url, headers=proxy_cloucd_headers).text.split(":57114\r\n")


def verify_ip_useful(ip):
    if not ip or ip == '':
        return False
    try:
        url = str.format(proxy_url, ip)
        response = requests.get(bin_ip_url, headers=proxy_cloucd_headers,
                                proxies={'http': url, 'https': url}).text
        json_res = json.loads(response)
    except requests.ConnectionError as ex:
        logging.error(ex)
        return False
    logging.info("ip: " + ip + " approved")
    rds.lpush(ip_proxy_list_key, ip)
    rds.setex(ip, 3 * 60, '1')
    return ip == json_res.get('origin')


def request_ip():
    ip = get_ip_proxies(150)
    ip_pool = []
    for i in ip:
        verify_ip_useful(i)
    return ip_pool


def get_ip():
    list_len = rds.llen(ip_proxy_list_key)
    ip = rds.lindex(ip_proxy_list_key, random.randint(0, list_len - 1))
    while rds.get(ip) is None:
        ip = rds.lrem(ip_proxy_list_key, list_len - 1, ip)
    return ip


if __name__ == "__main__":
    while True:
        if rds.llen(ip_proxy_list_key) < 100:
            request_ip()
        logging.info("ip pool size is -------:", rds.llen(ip_proxy_list_key))
        time.sleep(30)