import logging
import time

import redis
from pymysql.converters import escape_string

from micro_blog.DTO import Comments, User
from micro_blog.config import proxy_cloucd_headers
from micro_blog.get_ip import get_response
from micro_blog.mblog_spider import cursor, conn

rds = redis.StrictRedis(host='127.0.0.1', port=6379, db=2, decode_responses=True)


comment_base_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'

comment_next_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_mid_list():
    sql = "select mid from status group by mid"
    rows = cursor.execute(sql)
    result = cursor.fetchmany(rows)
    res = set()
    for i in result:
        res.add(i[0])
    logging.info(res)
    return res


def insert_comment(cid, bid, created_at, like_count, text, source, user):
    sql = "insert into `comment` (`cid`, `bid`, `created_at`, `like_count`, `text`, `source`, `user`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (cid, bid, created_at, like_count, text, source, user)
    cursor.execute(sql)
    conn.commit()


def request_comment_url():
    mid_list = get_mid_list()
    for i in mid_list:
        comment_url = comment_base_url.format(i, i)
        if rds.get(comment_url) is not None:
            continue
        rds.setex(comment_url, 60 * 60 * 10, '1')
        response = get_response(comment_url, headers=proxy_cloucd_headers, retry_count=1)
        if response and response.json():
            json_res = response.json()
            explain_comment_list(json_res)
            while json_res is not None and json_res.get("data"):
                max_id = json_res.get("data").get("max_id")
                if max_id is None or max_id == '0':
                    break
                next_comment_url = comment_next_url.format(i, i, max_id)
                if rds.get(next_comment_url) is not None:
                    continue
                rds.setex(next_comment_url, 60 * 60 * 10, '1')
                next_response = get_response(next_comment_url, headers=proxy_cloucd_headers, retry_count=1)
                logging.info(next_comment_url + "\n" + response.text)
                if next_response and next_response.json():
                    explain_comment_list(next_response.json())
                time.sleep(0.6)
            time.sleep(0.6)


def explain_comment_list(json_res):
    if not json_res.get("data") or len(json_res.get("data")) == 0:
        return
    comment_list = json_res.get("data").get("data")
    for k in comment_list:
        u = k.get("user")
        user = User(u.get("id"), u.get('avatar_hd'), u.get('description'), u.get('follow_count'),
                    u.get("followers_count"), u.get('gender'), u.get('profile_url'), u.get('screen_name'))
        comment = Comments(k.get("id"), k.get("bid"), k.get("created_at"),
                           k.get("like_count"), escape_string(k.get("text")), k.get("source"), user.id)
        logging.info(comment.__dict__.items())
        try:
            insert_comment(comment.id, comment.bid, comment.created_at, comment.like_count, comment.text,
                           comment.source, comment.user)
        except:
            logging.error("insert error")
            continue
        time.sleep(0.5)


if __name__ == "__main__":
    request_comment_url()
