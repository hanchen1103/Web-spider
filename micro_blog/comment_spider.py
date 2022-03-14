import json.decoder
import logging
import time

import pymysql
import requests

from micro_blog.DTO import Comments, User
from micro_blog.mblog_spider import cursor, conn
from spider_jingdong import headers

comment_base_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0&page={}'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_mid_list():
    sql = "select mid from status group by mid"
    rows = cursor.execute(sql)
    result = cursor.fetchmany(rows)
    res = set()
    for i in result:
        res.add(i[0])
    return res


def insert_comment(cid, bid, created_at, like_count, text, source, user):
    sql = "insert into `comment` (`cid`, `bid`, `created_at`, `like_count`, `text`, `source`, `user`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (cid, bid, created_at, like_count, text, source, user)
    cursor.execute(sql)
    conn.commit()


def request_comment_url():
    mid_list = get_mid_list()
    for i in mid_list:
        for j in range(1, 100):
            comment_url = comment_base_url.format(i, i, j)
            response = requests.get(comment_url, headers=headers)
            if response.status_code != 200:
                continue
            try:
                json_res = response.json()
            except json.decoder.JSONDecodeError as e:
                logging.error(e)
                continue
            if json_res:
                if not json_res.get("data") or len(json_res.get("data")) == 0:
                    break
                comment_list = json_res.get("data").get("data")
                for k in comment_list:
                    u = k.get("user")
                    user = User(u.get("id"), u.get('avatar_hd'), u.get('description'), u.get('follow_count'),
                                u.get("followers_count"), u.get('gender'), u.get('profile_url'), u.get('screen_name'))
                    comment = Comments(k.get("id"), k.get("bid"), k.get("created_at"),
                                       k.get("like_count"), k.get("text"), k.get("source"), user.id)
                    logging.info(comment.__dict__.items())
                    try:
                        insert_comment(comment.id, comment.bid, comment.created_at, comment.like_count, comment.text,
                                   comment.source, comment.user)
                    except:
                        logging.error("insert error")
                        continue
                    time.sleep(1)


if __name__ == "__main__":
    request_comment_url()
