import json

import pymongo
from pandas import DataFrame
from pymongo import MongoClient
import requests
import re
import time
import urllib
from bs4 import BeautifulSoup


#每50个帖子一页
def pagination(num):
    num = int(num)
    if num%50 == 0:
        page = num //50 #整数除法
        # print(page)
    else:
        page = num // 50+1
        # print(page)
    print("页面数：", page)
    return page

#找到所有帖子进行分页
def all_page(num, url):
    """
    :param num:主题贴吧中的帖子个数
    :param url:主题贴吧的链接个数
    :return:
    """
    # print(url)
    number = pagination(num)
    # print(number)
    array =map(lambda x: (x-1)*50, range(1, number+1)) # map返回的结果是迭代器(iterator)
    # print(list(array))   #将迭代器产生的值放入list中

    array =list(array)
    # print(array)
    address = map(lambda x: (url + '&pn=' + str(x)), array)
    address = list(address)
    # print(address)
    return address


# base_url = "http://tieba.baidu.com/f?fr=wwwt&kw="

#获取话题(关键字)的连接
def baidu_url(url):

    """
    :param url: 主题贴吧的链接
    :return:

    """
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': header}
    # url = "https://tieba.baidu.com/f?ie=utf-8&kw=%E4%B8%8A%E6%B5%B7%E5%A4%96%E9%AB%98%E6%A1%A5%E9%80%A0%E8%88%B9%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&fr=search"
    request = requests.get(url, headers=headers)
    # print("获取网页连接:状态码", request.status_code)
    if request.status_code == 200:
        request =request.text
        # print("文本内容：", request)
        count = re.compile(r'<span class="red_text">(.*?)</span>个，贴子数.*')
        # print("主题数", count)
        number = re.search(string=request, pattern=count)
        # print("主题贴吧数：",number.group(1))
        try:
            number = int(number.group(1))
            print("主题贴吧数:", number)
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
    print("各个页面链接为：", urllists)
    return urllists


#获取所有帖子链接
def tieba(url):
    """
    :param url: 页面的链接
    :return:
    """
    header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    headers = {"User-Agent": header}
    array = []
    nurls = baidu_url(url)
    for nurl in nurls:
        res = requests.get(nurl, headers=headers)
        # print("帖子链接的状态码：", res.status_code)
        if res.status_code == 200:
            res = res.text
            pattern = re.compile(r'<a (.*?)href="(.*?)"(.*?)title="(.*?)"(.*?)class="j_th_tit "')
            # print(pattern)
            # pattern = re.compile(r'a (.*?)href = "(.*?)"(.*?)title = "(.*?)" (.*?)class = "j_th_tit"')
            rest = re.findall(string=res, pattern=pattern)
            # print("该页有的贴吧信息条数：", len(rest))
            for result in rest:
                # print(result[1], result[3])

                #点进去帖子的链接
                new_url = "https://tieba.baidu.com"+result[1]
                #array用来存储所有帖子的链接
                array.append(new_url)
            time.sleep(0.5)
        else:
            print("主题链接不存在")
            break
    return array

#获取贴吧中的帖子的内容
def get_content(searchword, CompanyName, url):
    """
    :param CompanyName: 公司名称
    :param searchword: 关键字搜索，例："造船"
    :param url:页面的链接
    :return:
    """
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': header}

    #获取所有帖子的链接
    tbs = tieba(url)

    print("所有的帖子的链接为：", tbs)
    print("帖子个数： ", len(tbs))
    for tb in tbs:
        res = requests.get(tb, headers=headers)
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
                continue
        else:
            continue
        return 0

def get_post(CompanyName, number, tb, headers):
    """
    :param CompanyName:公司名称
    :param number: 主题贴吧的帖子个数
    :param tb: 某一个帖子的链接
    :param headers: 头部信息
    :return:
    """
    # mongodb = "172.25.2.60"
    mongodb = "localhost"
    dbport = 27017
    conn = pymongo.MongoClient(mongodb, dbport)

    db = conn['eTensorDB']
    _table = db['Public_Entiment_TieBaInformation']
    pnlist = []
    list_content = []
    title = ""
    tb_url = ""

    for i in range(1, number + 1):
        # if i > 2:
        #     break
        tb_url = tb +"?pn="+str(i)
        if tb_url in pnlist and len(pnlist) > 0:
            break
        else:
            print("帖子的链接：", tb_url)
            # print(len(tb_url))
            req = requests.get(tb_url, headers=headers)
            rr = req.text
            html1 = BeautifulSoup(rr, "lxml") #html5lib
            div_ = html1.find('div', id="j_p_postlist")
            div_s = div_.find_all("div", class_="l_post")

            try:
                date_time = json.loads(div_s[0]['data-field'])['content']['date']
            except Exception as e:
                try:
                    date_time = div_s[0].find_all('span', class_='tail-info')[
                        len(div_s[0].find_all('span', class_='tail-info')) - 1].get_text()
                except Exception as e:
                    print(e)
                    date_time = ''

            #获取帖子的作者，内容，时间，最后添加的是一个这样的内容。
            comments =[]
            for div in div_s:
                dict ={}
                dict['comment_author'] = div.find("div", class_="d_author")\
                    .find("ul", class_="p_author").find("li", class_="d_name")\
                    .find("a").get_text()
                try:
                    dict["comment_datetime"] = json.loads(div["data-field"]["content"]["date"])
                except:
                    # dict["comment_datetime"] = div.find("div", class_="d_post_content_main")\
                    #     .find("div", class_="core_reply").find("div", class_="post-tail-wrap")\
                    #     .find("span", class_="tail-info")[2].get_text()
                    dict["comment_datetime"] = ''
                dict["comment_content"] = div.find("div", class_="d_post_content").get_text().replace(" ", "")
                # print(dict)

                comments.append(dict)

            #获取帖子的标题
            try:
                post_name = html1.find("div", id="j_core_title_wrap").find("h3").get_text()
                print("帖子主题：", post_name)
            except:
                post_name =""
            Data = {"Post_Name": post_name, "Post_Content": comments, "url": tb_url,
                    "Company_Name": CompanyName, "Source": "贴吧", 'publish_date': date_time}

            print(Data)
            _table.update_one({'Post_Name': post_name}, {'$set': Data}, True)
            return True

# https://tieba.baidu.com/f?kw=上海外高桥造船有限公司 + &pn= + 50
# baidu_url("https://tieba.baidu.com/f?kw=%E4%B8%8A%E6%B5%B7%E5%A4%96%E9%AB%98%E6%A1%A5%E9%80%A0%E8%88%B9%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8")

# get_content("上海外高桥造船有限公司", "造船", "https://tieba.baidu.com/f?kw=%E4%B8%8A%E6%B5%B7%E5%A4%96%E9%AB%98%E6%A1%A5%E9%80%A0%E8%88%B9%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8")


def impotpost(searchword, CompanyName):
    baseUrl = 'https://tieba.baidu.com/f'
    data = {'kw': CompanyName, 'ie': "utf-8"}

    #将后缀进行编码
    data = urllib.parse.urlencode(data)
    # print(data)
    url = baseUrl+"?"+data
    # print(url)

    #依据链接爬取网页中的帖子
    get_content(searchword, CompanyName, url)
#举例
# impotpost("造船行业", "上海外高桥造船有限公司")


#获取企业的别称
def get_all_company_and_alias():
    client = pymongo.MongoClient('172.25.2.60', 27017)
    db = client['eTensorDB']
    col = db['Company_Analysis']
    cursors = col.find()
    company_name_alais = []
    for cursor in cursors:
        dict_ = {}
        dict_['company_name'] = cursor['company_name']
        alias = []
        alias_dict = cursor['alias']
        if alias_dict :
            for i in alias_dict:
                alias.append(i)
        # print(alias)
        dict_['alias'] = alias
        company_name_alais.append(dict_)
        # print(company_name_alais)
    return company_name_alais

def _get_all_company():
    """
    :return:返回类型list，具体包括公司名称和别称
    """
    client = pymongo.MongoClient("172.25.2.60", 27017)
    db = client['eTensorDB']
    collection =db["Company_Basic_Information"]
    cursors = collection.find({'Get_Company': re.compile('船')})
    company_name_alias = []
    for cursor in cursors:
        dict_ = {}
        dict_["company_name"] = cursor["Get_Company"]
        alias = []
        alias_dict = cursor["alias"]
        if alias_dict:
            for key in alias_dict:
                alias.append(key)

        dict_['alias'] = alias
        company_name_alias.append(dict_)
    return company_name_alias


#依据关键字和公司名称进行搜索
def start_update():
    alias = _get_all_company()
    for item in alias:
        alias = item['alias']
        company_name = item['company_name']
        if alias:
            for a_item in alias:
                print('item: ', a_item)
                impotpost(a_item, company_name)
        else:
            print('item: ', company_name)
            impotpost(company_name, company_name)

import csv
if __name__ == "__main__":
    alias = _get_all_company()

    for item in alias:
        alias = item['alias']
        company_name = item['company_name']
        # print(company_name, alias)
        if alias:
            for a_item in alias:
                print(company_name, "存在alias, 搜索item: ", a_item)
                impotpost('《' + a_item + '》', company_name)
        else:
            print(company_name, '不存在alias, 搜索item为: ', company_name)
            impotpost('《'+company_name + '》', company_name)
            continue