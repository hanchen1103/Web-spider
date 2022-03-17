import requests

from micro_blog.config import bin_ip_url, proxy_cloucd_headers



# ip = '121.233.226.70:35342'

# response = requests.get(bin_ip_url, headers=proxy_cloucd_headers,
#                                 proxies={'http': 'http://' + ip, 'https': 'https://' + ip}).json()
from micro_blog.get_ip import get_response

resp = get_response(bin_ip_url, headers=proxy_cloucd_headers, retry_count=0).json()

print(resp)



