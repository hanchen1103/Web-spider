import json
import logging
import pymysql
import re
import time
import requests
from pymysql.converters import escape_string

from micro_blog.DTO import User, Page_info, Status
from micro_blog.config import proxy_cloucd_headers
from micro_blog.explain_url import rds, headers
from micro_blog.get_ip import get_ip, get_ip_proxy, get_response
from micro_blog.single_blog import BLOG_URL_LIST, request_and_explain_blog

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

status_origin_url = 'https://m.weibo.cn/statuses/show?id='

conn = pymysql.connect(host="localhost", user="root", password="lyp82ndlf", database="blog", port=3306)

cursor = conn.cursor()


def get_blog_url():
    blog_list = rds.get(BLOG_URL_LIST)
    if blog_list is None:
        request_and_explain_blog()
    return json.loads(rds.get(BLOG_URL_LIST))


def get_bid(url):
    return re.search(r'https.*?mblogid=(.*?)&.*', url).groups()[0]


def insert_user(user_id, avatar_hd, description, follow_count, followers_count, gender, profile_url, screen_name):
    sql = "insert into `user` (`user_id`, `avatar_hd`, `description`, `follow_count`, `followers_count`, `gender`, `profile_url`, `screen_name`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (user_id, avatar_hd, description, follow_count, followers_count, gender, profile_url, screen_name)
    cursor.execute(sql)
    conn.commit()


def insert_page_info(mid, content1, content2, page_url, page_title, play_count, title, type, urls):
    sql = "insert into `page_info` (`mid`, `content1`, `content2`, `page_url`, `page_title`, `play_count`, `title`, `type`, `urls`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (mid, content1, content2, page_url, page_title, play_count, title, type, urls)
    cursor.execute(sql)
    conn.commit()


def insert_status(bid, w_id, mid, attitudes_count, reposts_count, comments_count, created_at, edit_at, text, raw_text,
                  user,
                  page_info, pic_str):
    sql = "insert into `status` (`bid`, `w_id`, `mid`, `attitudes_count`, `reposts_count`, `comments_count`, `created_at`, `edit_at`, `m_text`, `raw_text`, `user`, `page_info`, `pic_str`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s')" \
          % (bid, w_id, mid, attitudes_count, reposts_count, comments_count, created_at, edit_at, text, raw_text, user,
             page_info, pic_str)
    cursor.execute(sql)
    conn.commit()


def request_blog_and_explain():
    blog_list = get_blog_url()
    for i in blog_list:
        mblog_id = get_bid(i)
        if not mblog_id:
            continue
        status_url = status_origin_url + mblog_id
        try:
            response = get_response(status_url, headers=proxy_cloucd_headers, retry_count=1)
            if response and response.json():
                json_res = response.json()
                if json_res and json_res.get('data'):
                    items = json_res.get('data')
                    u = items.get('user')
                    if u:
                        user = User(u.get("id"), u.get('avatar_hd'), u.get('description'), u.get('follow_count'),
                                    u.get("followers_count"), u.get('gender'), u.get('profile_url'), u.get('screen_name'))
                        logging.info(user.__dict__.items())
                        insert_user(user.id, user.avatar_hd, escape_string(user.description), user.follow_count,
                                    user.followers_count,
                                    user.gender, user.profile_url, escape_string(user.screen_name))
                    p = items.get("page_info")
                    if p:
                        p_str = ""
                        if p.get("urls"):
                            p_str = json.dumps(p.get("urls"))
                        page_info = Page_info(items.get("mid"), p.get("content1"), p.get("content2"), p.get("page_url"),
                                              p.get("page_title"),
                                              p.get("play_count"), p.get("title"), p.get("type"), p_str)
                        logging.info(page_info.__dict__.items())
                        insert_page_info(page_info.mid, escape_string(page_info.content1),
                                         escape_string(page_info.content2), page_info.page_url,
                                         escape_string(page_info.page_title),
                                         page_info.play_count, escape_string(page_info.title), page_info.type,
                                         page_info.urls)
                    pics = items.get("pics")
                    pic_str = ' '
                    if pics:
                        for k in pics:
                            pic_str += k.get("url") + "\n"
                    pifo_mid = " "
                    if p:
                        pifo_mid = p.get("mid")
                    status = Status(items.get("bid"), items.get("id"), items.get("mid"), items.get("attitudes_count"),
                                    items.get("reposts_count"), items.get("comments_count"), items.get("created_at"),
                                    items.get("edit_at"), items.get("text"), items.get("raw_text"), u.get("id"), pifo_mid,
                                    pic_str)
                    logging.info(status.__dict__.items())
                    insert_status(status.bid, status.id, status.mid, status.attitudes_count,
                                  status.reposts_count, status.comments_count, status.created_at, status.edit_at,
                                  escape_string(status.text), escape_string(status.raw_text), status.user,
                                  escape_string(status.page_info), escape_string(status.pics))
                    time.sleep(1.5)
        except requests.ConnectionError as e:
            logging.error(e)


if __name__ == "__main__":
    request_blog_and_explain()
