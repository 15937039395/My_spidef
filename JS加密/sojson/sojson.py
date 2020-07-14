#以中国人民银行为例，破解sojison
import requests,execjs,datetime,time,re
from fake_useragent import UserAgent


#实例化session
session = requests.session()
#获取随机请求头
def getUA():
    headers = {
        "User-Agent": UserAgent().random,
    }
    return headers


def spider():
    url='http://www.pbc.gov.cn/tiaofasi/144941/144957/index.html'

    resp=session.get(url).text
    js = re.findall('<script type="text/javascript">(.*?)</script>', resp,re.DOTALL)[0]
    ll = re.sub("window\[_0x56ae\('0x3c','\)9A&'\)\]=_0x35ace3;", "return _0x35ace3;", js)
    ctx = execjs.compile(ll)
    href = ctx.call('_0x33f22a')
    new_url="http://www.pbc.gov.cn"+href
    zhuye = session.get(url=new_url)
    print(zhuye.content.decode())



if __name__ == '__main__':
    spider()
