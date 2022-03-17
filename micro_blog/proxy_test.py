import requests

from micro_blog.config import bin_ip_url, proxy_cloucd_headers
from micro_blog.get_ip import get_ip

ip = get_ip()

print(ip)
# ip = '121.233.226.70:35342'

response = requests.get(bin_ip_url, headers=proxy_cloucd_headers,
                                proxies={'http': 'http://' + ip, 'https': 'https://' + ip}).json()

print(response)


