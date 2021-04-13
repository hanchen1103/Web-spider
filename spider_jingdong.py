import requests
from bs4 import BeautifulSoup
import time

headers = {
    'Cookie':'__jda=122270672.918638549.1617224168.1617228928.1617275005.3; unpl=V2_ZzNtbUBWShZ0ChVRck5cAGICFlVLUxFFJgBEAXsQDwVhAkFaclRCFnUUR1FnGFwUZgYZWUVcQhNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHMZVQJlChZYSmdzEkU4dlN7GFgNZTMTbUNnAUEpC0NSfRtbSG8DG1pAXkcQfThHZHg%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_308203b48f14405985cab93d18b170b6|1617224169640; __jdu=918638549; areaId=12; ipLoc-djd=12-904-907-50559; PCSYCityID=CN_0_0_0; shshshfp=a450d4144d0da71318a9e89d2a125d3c; shshshfpa=e3c95eb3-3cc7-b2ca-2389-726a7f068c67-1617224171; shshshfpb=s4ujeCFYmGfKAgwl9KM2a0A%3D%3D; qrsc=3; user-key=b807a3ec-7ee5-4996-90a7-f09be3c9e2e6; cn=0; __jdb=122270672.1.918638549|3.1617275005; __jdc=122270672; shshshsID=89aacfe8771e28f2594dc35b68702e4a_1_1617275005522; rkv=1.0; 3AB9D23F7A4B3C9B=U2SQE4TTPPBQ33X3QZR5VQDZGEZPFUSYHSZBMHU4DAGIQEM55IEGPJA62GXCEH4WNNFDLYQKHMRGFQ3OH3UDQGV2YI',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
}

kv = {
    "keyword": "情趣内衣",
    "page":"2"
}

map = {}

res = []

def get_all():
    html = requests.get("https://search.jd.com/Search", headers=headers, params=kv)
    bs = BeautifulSoup(html.text, 'html.parser')

    list = bs.find_all("div", id="J_goodsList")[0]

    rs = list.find_all("div", class_="gl-i-wrap")

    for _ in rs:
        u = _.a.attrs['href']
        price = _.strong.i
        map["https:" + str(u)] = str(price).replace("<i>", "").replace("</i>", "")


def get_infor():
    get_all()
    t_map = {}
    for k, v in map.items():
        time.sleep(0.3)
        html = requests.get(k, headers=headers)

        bs = BeautifulSoup(html.text, "html.parser")
        tag = bs.find_all('div', class_='p-parameter')[0]
        pic = bs.find_all('div', class_='J-addcart-mini EDropdown')[0]

        band = tag.find('li').attrs['title']
        pic_url = pic.find('img').attrs['src']

        list = tag.find_all('li')

        str = ''

        for i in list:
            if (i.string != None):
                str += i.string

        t_map['band'] = band
        t_map['info'] = str
        t_map['url'] = k
        t_map['price'] = v
        t_map['pic'] = pic_url
        print(t_map.items())
        res.append(t_map)

if __name__ == "__main__":
    get_infor()




