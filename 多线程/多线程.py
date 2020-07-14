import redis,json,re,datetime,time,requests,random,queue
from threading import Thread
import pyodbc
import os

from fake_useragent import UserAgent

#数据库
def Sqlserver():
    cnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=10.10.1.56;DATABASES=databases;UID=sasa;PWD=r2@2008;charset='utf8'")
    cursor = cnxn.cursor()
    return cursor



from lxml import etree
def readfile(path):              # 读取文件的函数
    content = [line.strip() for line in open(path, encoding='utf-8',errors='ignore').readlines()]
    return content
def savefile(savepath,content):  # 保存文件的函数
    fp = open(savepath,'a+',encoding='utf-8',newline="",errors='ignore')
    fp.write(content+"\r\n")
    fp.close()




#####################################################################随机请求头#####################################################################
def getUA():
    headers = {
        "User-Agent": UserAgent(use_cache_server=False).random,
    }
    return headers

#####################################################################解析响应返回resp数据#####################################################################
def getResp(url,data=None):
    rep=None
    for i in range(6):
        try:
            if data:
                rep = requests.post(url, headers=getUA(),data=data,timeout=10)
            else:
                rep = requests.get(url, headers=getUA(),timeout=10)
            if rep.status_code == 200:
                #正常请求,不打印数据
                break
        except Exception as ex:
            print('第%s次请求' % i, url)
            if i==4:
                print('错误请求超过四次,保存日志')
                nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                err = '%s%s:%s==>%s' % (nowTime, Exception, ex, url)
                print(err)
    return rep

item={}


def Consumer(url):
    resp = getResp(url)
    try:
        respon = resp.content.decode('utf-8')
    except:
        respon = ''

    #########################################解析数据#########################################
    try:
        html = etree.HTML(respon)
    except:
        html = ''

    #########################################提取字段#########################################
    item['url'] = url

    try:
        item['MPN'] = html.xpath('//*[@id="maincontent"]/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div[1]/div/span/text()')[0]
    except:
        item['MPN'] = ''
    print(item)




if __name__ == "__main__":
    # 这里是队列
    q = queue.Queue(100)
    class Work(Thread):
        def run(self):
            while True:
                Consumer(q.get())
                #如果队列为空,则结束线程
                if q.empty():
                    break

    # 这里是控制线程数
    for i in range(10):
        Work().start()

    try:
        #从数据库中读取任务添加到队列中
        list_urls = Sqlserver().execute('SELECT * FROM Manufacturers_dataGordon.dbo.Sunscopeusa_url')
        for urls in list_urls:
            urls = list(urls)[0]
            q.put(urls)
    except Exception as e:
        print('添加任务到队列异常',e)



