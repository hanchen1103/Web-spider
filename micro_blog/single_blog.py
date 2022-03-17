import json
import logging
import time
import requests

from micro_blog.config import proxy_cloucd_headers
from micro_blog.explain_url import rds, get_xhr_url, XHR_URL_LIST_KEY, headers
from micro_blog.get_ip import get_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BLOG_URL_LIST = 'blog-url-list'

CONTAIN_STRING = 'status'


def get_url_list():
    data = rds.get(XHR_URL_LIST_KEY)
    if data is None:
        get_xhr_url()
    url_list = json.loads(rds.get(XHR_URL_LIST_KEY))
    return url_list


def request_and_explain_blog():
    xhr_list = get_url_list()
    blog_url = set()
    for _ in xhr_list:
        try:
            response = get_response(_, headers=proxy_cloucd_headers, retry_count=0)
            if response and response.json:
                json_res = response.json()
                items = json_res.get('data').get('cards')
                for i in items:
                    if i.get('card_group'):
                        for j in i.get('card_group'):
                            if j.get('scheme') and CONTAIN_STRING in j.get('scheme'):
                                logging.info(j.get('scheme'))
                                blog_url.add(j.get('scheme'))
                    if i.get('scheme') and CONTAIN_STRING in i.get('scheme'):
                        logging.info(i.get('scheme'))
                        blog_url.add(i.get('scheme'))
                time.sleep(1.5)
        except requests.ConnectionError as e:
            logging.error(e)
    rds.setex(BLOG_URL_LIST, 60 * 60 * 16, json.dumps(list(blog_url)))
    return blog_url


if __name__ == "__main__":
    request_and_explain_blog()
