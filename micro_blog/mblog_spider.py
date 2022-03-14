import json
import logging
import pymysql
import re
import time
import requests

from micro_blog.DTO import User, Page_info, Status
from micro_blog.explain_url import rds, headers
from micro_blog.single_blog import BLOG_URL_LIST, request_and_explain_blog

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

status_origin_url = 'https://m.weibo.cn/statuses/show?id='

conn = pymysql.connect(host="localhost", user="root", password="lyp82ndlf", database="blog", port=3306)

cursor = conn.cursor()


def get_blog_url():
    blog_list = rds.get(BLOG_URL_LIST)
    if blog_list is None:
        request_and_explain_blog()
    return json.loads(blog_list)


def get_bid(url):
    return re.search(r'https.*?mblogid=(.*?)&.*', url).groups()[0]


def insert_user(user_id, avatar_hd, description, follow_count, followers_count, gender, profile_url, screen_name):
    sql = "insert into `user` (`user_id`, `avatar_hd`, `description`, `follow_count`, `followers_count`, `gender`, `profile_url`, `screen_name`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (user_id, avatar_hd, description, follow_count, followers_count, gender, profile_url, screen_name)
    cursor.execute(sql)
    conn.commit()


def insert_page_info(content1, content2, page_url, page_title, play_count, title, type, urls):
    sql = "insert into `page_info` (`content1`, `content2`, `page_url`, `page_title`, `play_count`, `title`, `type`, `urls`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (content1, content2, page_url, page_title, play_count, title, type, urls)
    cursor.execute(sql)
    conn.commit()


def insert_status(bid, w_id, mid, attitudes_count, reposts_count, comments_count, created_at, edit_at, raw_text, user,
                  page_info, pic_str):
    sql = "insert into `status` (`bid`, `w_id`, `mid`, `attitudes_count`, `reposts_count`, `comments_count`, `created_at`, `edit_at`, `raw_text`, `user`, `page_info`, `pic_str`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s')" \
          % (bid, w_id, mid, attitudes_count, reposts_count, comments_count, created_at, edit_at, raw_text, user,
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
            response = requests.get(status_url, headers=headers)
            if response.status_code != 200:
                continue
            json_res = response.json()
            if json_res and json_res.get('data'):
                items = json_res.get('data')
                u = items.get('user')
                if u:
                    user = User(u.get("id"), u.get('avatar_hd'), u.get('description'), u.get('follow_count'),
                                u.get("followers_count"), u.get('gender'), u.get('profile_url'), u.get('screen_name'))
                    logging.info(user.__dict__.items())
                    insert_user(user.id, user.avatar_hd, user.description, user.follow_count, user.followers_count,
                                user.gender, user.profile_url, user.screen_name)
                p = items.get("page_info")
                if p:
                    page_info = Page_info(p.get("content1"), p.get("content2"), p.get("page_url"), p.get("page_title"),
                                          p.get("play_count"), p.get("title"), p.get("type"), p.get("urls"))
                    logging.info(page_info.__dict__.items())
                    insert_page_info(page_info.content1, page_info.content2, page_info.page_url, page_info.page_title,
                                     page_info.play_count, page_info.title, page_info.type, page_info.urls)
                pics = items.get("pics")
                pic_str = ''
                if pics:
                    for k in pics:
                        pic_str += k.get("url") + "\n"
                status = Status(items.get("bid"), items.get("id"), items.get("mid"), items.get("attitudes_count"),
                                items.get("reposts_count"), items.get("comments_count"), items.get("created_at"),
                                items.get("edit_at"), items.get("raw_text"), user.id, page_info.title, pic_str)
                logging.info(status.__dict__.items())
                insert_status(status.bid, status.id, status.mid, status.attitudes_count,
                              status.reposts_count, status.comments_count, status.created_at, status.edit_at,
                              status.raw_text, status.user, status.page_info, status.pics)
        except requests.ConnectionError as e:
            logging.error(e)
        time.sleep(2)


if __name__ == "__main__":
    request_blog_and_explain()
