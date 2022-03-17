import logging

import requests

from micro_blog.config import local_proxies
from micro_blog.get_ip import get_ip_proxy

base_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D38%26q%3D%E8%BF%94%E4%B9%A1%E5%B0%B1' \
           '%E4%B8%9A%26t%3D0&page_type=searchall&page='

headers = {
    'authority': 'm.weibo.cn',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    'cookie': 'WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn; SUB=_2A25PKzyhDeRhGeFL4lES9i7IyD2IHXVs1ETprDV6PUJbktCOLRbSkW1NfZMpKoUN2ElhNGb2eC3x-hiXmHS3ToW3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhHzIJ6u8LvYivz9NMHSE9A5NHD95QNSK.0e0q7ShepWs4DqcjSeCH81FHFxCHFesSoq7tt; SSOLoginState=1647267057; _T_WM=66006514846; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=5df71f; M_WEIBOCN_PARAMS=oid%3D4745789555344018%26luicode%3D10000011%26lfid%3D100103type%253D38%2526q%253D%25E8%25BF%2594%25E4%25B9%25A1%25E5%25B0%25B1%25E4%25B8%259A%2526t%253D0%26fid%3D100103type%253D1%2526q%253D%25E8%25BF%2594%25E4%25B9%25A1%25E5%25B0%25B1%25E4%25B8%259A%26uicode%3D10000011',
    'x-requested-with': 'XMLHttpRequest',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'refer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E8%BF%94%E4%B9%A1%E5%B0%B1%E4%B8%9A'
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_url(end):
    url_list = []
    for i in range(1, end):
        url_list.append(base_url + str(i))
    return url_list


def get_request():
    url_list = get_url(3)
    response = []
    for _ in url_list:
        try:
            proxy = get_ip_proxy()
            logging.info("request ip is: " + str(proxy))
            request = requests.get(_, headers=headers, proxies=proxy, timeout=5, verify=False)
            while request.status_code != 200:
                proxy = get_ip_proxy()
                logging.info("request ip is: " + str(proxy))
                request = requests.get(_, headers=headers, proxies=proxy, timeout=5, verify=False)
            response.append(request.json())
        except requests.ConnectionError as e:
            logging.info("use local ip---")
            request = requests.get(_, headers=headers, proxies=local_proxies, timeout=10, verify=False)
            response.append(request.json())
            logging.info(e)
        finally:
            logging.info(response)
    return response


# 获取此话题下的所有微博
def dump_json_get_url():
    scheme_list = []
    response_list = get_request()
    for i in response_list:
        if i:
            items = i.get('data').get('cards')
            for j in items:
                card_list = j.get('card_group')
                for k in card_list:
                    scheme_list.append(k.get('scheme'))
    logging.info(scheme_list)
    return scheme_list


if __name__ == "__main__":
    print(len(dump_json_get_url()))