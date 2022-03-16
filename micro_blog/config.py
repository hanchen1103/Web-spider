proxy_cloud_account = "17851627776"

proxy_cloud_password = "lyp82ndlf"

proxy_port = 57114

proxy_url = "http://" + proxy_cloud_account + ":" + proxy_cloud_password + "@{}" + ":" + "%d" % proxy_port

ip_proxy_list_key = 'ip-proxy-list'

proxy_cloucd_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

get_ip_url = "http://17851627776.v4.dailiyun.com/query.txt?key=NPX026636D&word=&count={}&rand=false&ltime=0&norepeat=false&detail=false"

bin_ip_url = 'http://httpbin.org/ip'
