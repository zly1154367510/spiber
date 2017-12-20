#coding=utf-8
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import random_headers
from bs4 import BeautifulSoup as bs
import urllib2
from multiprocessing import Pool
import time
import pymysql
import urllib




pages = 1
conn = pymysql.connect(host="localhost", port=3306, user="root", password="", database="cc")
curr = conn.cursor()
def get_proxy_ip(page):
    url = "http://www.xicidaili.com/nn/"+`page`
    headers = {"User-Agent":random_headers.get_random_headers()}
    request = urllib2.Request(url=url,headers=headers)
    html = urllib2.urlopen(request)
    soup = bs(html,"html.parser")
    findIps = soup.select("#ip_list > tr > td")
    for i in range(1,len(findIps),10):
        print "写入"+findIps[i].text+":"+findIps[i+1].text+"中"

        curr.executemany("insert into cc (aa,duankou) values (%s,%s)",[(findIps[i].text,findIps[i+1].text)])
        conn.commit()

def get_ip_list():
    curr.execute("select * from cc")
    res = curr.fetchall()
    ipList = []
    for i in res:
        ipHost = "http://"+i[1]+":"+i[2]
        ipList.append(ipHost)
    return ipList



def text_ip(ip):

    ip_host = ip
    print `ip_host`+"设置ip1"
    ip_supprot = urllib2.ProxyHandler({"http": ip_host})
    print `ip_host` + "设置ip2"
    opener = urllib2.build_opener(ip_supprot)
    print `ip_host` + "设置ip3"
    urllib2.install_opener(opener)
    print `ip_host` + "设置ip完成"


    try:
        content = urllib2.urlopen("http://ip.chinaz.com/").read()
        soup = bs(content, "html.parser")
        list1 = soup.find("p", {"class", "getlist pl10"})
        print content
        print list1
        if list1 != None:
            print ip_host + "可以存在"
            with open("chengIp.txt", "a") as f:
                f.write(ip + "\n")
        else:
            print ip_host + "不可存在"
            ips = ip.split(":")[1].replace("//", "")
            curr.execute("delete from cc where aa=%s", ([ips]))
            conn.commit()
    except:
        print ip_host + "不可存在"
        ips = ip.split(":")[1].replace("//","")
        curr.execute("delete from cc where aa=%s",([ips]))
        conn.commit()




if __name__ == '__main__':
    ipList = get_ip_list()
    start = time.time()
    pool = Pool()
    pool.map(text_ip,ipList)
    pool.close()
    pool.join()

    print time.time() - start




    curr.close()
    conn.close()


