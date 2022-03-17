import requests

from micro_blog.comment_spider import explain_comment_list
from micro_blog.config import bin_ip_url, proxy_cloucd_headers



# ip = '121.233.226.70:35342'

# response = requests.get(bin_ip_url, headers=proxy_cloucd_headers,
#                                 proxies={'http': 'http://' + ip, 'https': 'https://' + ip}).json()
from micro_blog.get_ip import get_response

url = "https://m.weibo.cn/comments/hotflow?id=4657397299154252&mid=4657397299154252&max_id=139265175488607&max_id_type=0"
resp = get_response(url, headers=proxy_cloucd_headers, retry_count=0)
json_res = resp.json()
# explain_comment_list(json_res)



