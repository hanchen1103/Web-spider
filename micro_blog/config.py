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

local_proxies = {
    "http": "http://127.0.0.1:1087",
    "htttps:": "https://127.0.0.1:1097",
}

dragonfly_ip = "https://proxyapi.horocn.com/api/v2/proxies?order_id=BQ6X1727559281466908&num=20&format=json&line_separator=win&can_repeat=yes&user_token=a40b1a65b555d28c7c0973e81680be00"

retry_count = 6