import logging

import requests

from micro_blog.get_request import dump_json_get_url

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    'cookie': 'WEIBOCN_WM=3349; H5_wentry=H5; backURL=https://weibo.cn; SUB=_2A25PKzyhDeRhGeFL4lES9i7IyD2IHXVs1ETprDV6PUJbktCOLRbSkW1NfZMpKoUN2ElhNGb2eC3x-hiXmHS3ToW3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhHzIJ6u8LvYivz9NMHSE9A5NHD95QNSK.0e0q7ShepWs4DqcjSeCH81FHFxCHFesSoq7tt; SSOLoginState=1647267057; WEIBOCN_FROM=1110006030; MLOGIN=1; _T_WM=54413996836; XSRF-TOKEN=698f13; M_WEIBOCN_PARAMS=luicode=10000011&lfid=100103type%3D38%26q%3D%E8%BF%94%E4%B9%A1%E5%B0%B1%E4%B8%9A%26t%3D0&oid=4635268570678869&fid=231522type%3D1%26t%3D10%26q%3D%23%E5%B0%8F%E9%95%87%E9%9D%92%E5%B9%B4%E8%BF%94%E4%B9%A1%E5%B0%B1%E4%B8%9A%E4%B8%BA%E4%BD%95%E6%88%90%E8%B6%8B%E5%8A%BF%23&uicode=10000011',
    'accept-language': 'zh-CN,zh;q=0.9',
}

MAX_PAGE = 200


def get_xhr_url_base():
    url_list = dump_json_get_url()
    api_url = 'https://m.weibo.cn/api/container/getIndex?'
    api_suffix = '&page_type=searchall&page='
    xhr_request = []
    for url in url_list:
        suffix_field = url.split("https://m.weibo.cn/search?")[1]
        request_api = api_url + suffix_field + api_suffix
        xhr_request.append(request_api)
    return xhr_request


def get_xhr_url():
    api_list = get_xhr_url_base()
    all_url = []
    for api in api_list:
        for i in range(0, MAX_PAGE):
            current_url = api + str(i)
            try:
                response = requests.get(current_url)
                if response.status_code != 200:
                    continue
                else:
                    json_res = response.json()
                    if json_res:
                        items = json_res.get('data').get('cards')
                        if items is None or len(items) == 0:
                            break
                        logging.info(current_url)
                        all_url.append(current_url)
            except requests.ConnectionError as e:
                logging.error(e)
    return all_url


if __name__ == "__main__":
    get_xhr_url()
