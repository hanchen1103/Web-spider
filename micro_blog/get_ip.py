import json
import logging
import random
import time

import redis
import requests

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
    ip = rds.lindex(ip_proxy_list_key, random.randint(1, rds.llen(ip_proxy_list_key) - 1))
    while ip and rds.get(str(ip).strip('\'')) is None:
        logging.info("redis delete ip is: " + ip)
        rds.lrem(ip_proxy_list_key, 1, ip)
        ip = rds.lindex(ip_proxy_list_key, random.randint(0, rds.llen(ip_proxy_list_key) - 1))
    return ip.strip('\'')


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
            print(ip)
            print(verify_ip_useful(ip))

def replenish_ip_pool():
    
if __name__ == "__main__":

    get_dragonfly_ip()
