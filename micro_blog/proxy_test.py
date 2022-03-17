import requests

from micro_blog.config import bin_ip_url, proxy_cloucd_headers



# ip = '121.233.226.70:35342'

# response = requests.get(bin_ip_url, headers=proxy_cloucd_headers,
#                                 proxies={'http': 'http://' + ip, 'https': 'https://' + ip}).json()
from micro_blog.get_ip import get_response

url = "https://m.weibo.cn/status/I0bOB7mUs?mblogid=I0bOB7mUs&luicode=10000011&lfid=231522type%3D1%26t%3D10%26q%3D%23%E8%BF%91%E4%B9%9D%E6%88%90%E9%9D%92%E5%B9%B4%E8%80%83%E8%99%91%E8%BF%87%E8%BF%94%E4%B9%A1%E5%B0%B1%E4%B8%9A%23"
resp = get_response(bin_ip_url, headers=proxy_cloucd_headers, retry_count=0).json()


print(resp)



