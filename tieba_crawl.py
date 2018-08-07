import json

import pymongo
from pymongo import MongoClient
import requests
import re
import time
import urllib
from bs4 import BeautifulSoup
MONDOGB = "localhost"
DBPORT = 27017
base_url = "http://tieba.baidu.com/f?fr=wwwt&kw="
#获取话题(关键字)的连接
def baidu_url(url):
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': header}
    # url = "https://tieba.baidu.com/f?ie=utf-8&kw=%E4%B8%8A%E6%B5%B7%E5%A4%96%E9%AB%98%E6%A1%A5%E9%80%A0%E8%88%B9%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&fr=search"
    request = requests.get(url, headers=headers)

    print("获取网页连接:状态码", request.status_code)

    if request.status_code == 200:
        request =request.text
        # print("文本内容：", request)
        count = re.compile(r'<span class="red_text">(.*?)</span>个，贴子数.*')
        # print("主题数", count)
        number = re.search(string=request, pattern=count)
        # print("主题贴吧数：",number.group(1))

        try:
            number = int(number.group(1))
            print("主题贴吧数", number)
        except:
            print('找不到贴吧')
            return []

        #只爬取前100
        if number >100:
            number = 100
        #主题的帖子个数以及主题的url
        urllists = all_page(str(number), url)
    else:
        print("error")
        urllists = []
    return urllists


#获取所有帖子链接
def tieba(url):
    header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    headers = {"User-Agent": header}
    array = []
    nurls = baidu_url(url)
    for nurl in nurls:
        res = requests.get(nurl, headers=headers)
        print("帖子链接的状态码：", res.status_code)
        if res.status_code == 200:
            res = res.text
            pattern = re.compile(r'<a (.*?)href="(.*?)"(.*?)title="(.*?)"(.*?)class="j_th_tit "')
            print(pattern)
            # pattern = re.compile(r'a (.*?)href = "(.*?)"(.*?)title = "(.*?)" (.*?)class = "j_th_tit"')
            rest = re.findall(string=res, pattern=pattern)
            print("该页有的贴吧信息条数：", len(rest))
            for result in rest:
                print(result[1], result[3])

                #点进去帖子的链接
                new_url = "https://tieba.baidu.com"+result[1]
                #array用来存储所有帖子的链接
                array.append(new_url)
            time.sleep(0.5)
        else:
            print("主题链接不存在")
            break
    return array

#每50个帖子进行分一页
def pagination(num):
    num = int(num)
    if num%50 == 0:
        page = num //50 #整数除法
        print(page)
    else:
        page = num // 50+1
        print(page)
    return page

#找到所有帖子进行分页
def all_page(num,url):
    number = pagination(num)
    array =map(lambda x:(x-1)*50,range(1,number+1)) # map返回的结果是迭代器(iterator)
    # print(list(array))   #将迭代器产生的值放入list中
    array =list(array)
    address = map(lambda x: (url + '&pn=' + str(x)), array)
    address = list(address)
    print(address)
    return address

#获取贴吧中的帖子的内容
def get_content(CompanyName,searword,url):
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': header}

    #获取所有帖子的链接
    tbs = tieba(url)

    print(tbs)
    for tb in  tbs:
        res= requests.get(tb, headers=headers)
        if res.status_code == 200:
            res = res.text
            ##这里可能会捕获不到
            count = re.compile(r'<span class="red">(.*?)</span>页.*')
            number = re.search(string=res, pattern=count)

            # 分页
            try:
                number = int(number.group(1))
            except Exception as e:
                print('找不到贴吧')
                continue

            # 判断重复
            if get_post(CompanyName, number, tb, headers):
                print("Succeed in climbing a post ! ")
        else:
            continue
        return 0

def get_post(CompanyName, number, tb, headers):
    conn = pymongo.MongoClient(MONGODB, DBPORT)

    db = conn['eTensorDB']
    _table = db['Public_Entiment_TieBaInformation']
    pnlist = []
    list_content = []
    title = ""
    tb_url = ""

    for i in range(1, number + 1):
        if i>2:
            break
        tb_url = tb +"?pn="+str(i)
        if tb_url in pnlist and len(pnlist) > 0:
            break
        else:
            print(tb_url)

            req = requests.get(tb_url, headers=headers)
            rr = req.text
            html1 = BeautifulSoup(rr, "lxml") #html5lib
            left_content = html1.find('div', id="j_p_postlist")
            left_content_in = left_content.find_all("div", class_="l_post")

            try:
                date_time = json.loads(left_content_in[0]['data-field'])['content']['date']
            except Exception as e:
                try:
                    date_time = left_content_in[0].find_all('span', class_='tail-info')[
                        len(left_content_in[0].find_all('span', class_='tail-info')) - 1].get_text()
                except Exception as e:
                    print(e)
                    date_time = ''
