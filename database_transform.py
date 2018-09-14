
# from mongoengine import *
#
# connect('eTensorDB', host='172.25.2.60', port=27017)
#
# class Company_Basic_Information(Document):
#     Company_Name = StringField()
#     Original_Web_Url = StringField()
#     Img = StringField()
#     Base_Information= ListField()
#     Product= ListField()
#     Get_Company= StringField()
#     Title_Information =ObjectIdField()
#     Essential_Information=ObjectIdField()
#     Investment_Abroad = ListField()
#     Legal_Proceedings =ListField()
#     Referee_Document =ListField()
#     Court_Announcement =ListField()
#     Person_Against =ListField()
#     Announcement =ListField()
#     alias =ObjectIdField()
#     industry = StringField()
#     latitude =ObjectIdField()
#     History_Name =StringField()
#     avatar=StringField()
#     intruduce=StringField()
#     account_name =StringField()
#     wei_xin_hao =StringField()
#     ewm_img = StringField()
#     article_href =StringField()
#     switch = StringField()
#
# users = Company_Basic_Information.objects.all() #返回所有的文档对象列表
# print(users)
# import pymongo as pymongo
#
import pymongo as pymongo
#
# client = pymongo.MongoClient('172.25.2.60', 27017)
# db = client['eTensorDB']
# collection = db['Company_Basic_Information']
#
# collecitons = collection.find({"industry": "造船"})
# a__=[]
#
# for item in collecitons:
#     # print(item["industry"])
#     item["industry"] = "船舶制造"
#     print(item)
#     a__.append(item)
#     # print(type(item))
#     # return item
# print(123, len(a__))

# import pymongo
#

#readme
#将mongodb"172.25.2.60"数据库eTensorDB的Company_Basic_Information表保存到别的数据库。
def get():

    client = pymongo.MongoClient('172.25.2.60', 27017)
    db = client['eTensorDB']
    collection = db['Company_Basic_Information']

    collecitons = collection.find({"industry": "造船"})

    giet = []
    for item in collecitons:
        # print(item["industry"])
        item["industry"] = "船舶制造"
        print(item)
        # print(type(item))
        print(234)
        #没获取一条数据，就进行保存
        pymongo.MongoClient("localhost", 27017)["database234"]['Company_Basic_Information'].insert(item)
        print(123)
        # return item

        # pymongo.MongoClient("localhost", 27017)["database"]['Company_Basic_Information'].save(item)


# def print():
#     MONGODB = "localhost"
#     PORT = 27017
#     client = pymongo.MongoClient(MONGODB, PORT)
#     db = client["database"]
#     zhihu_col = db['Company_Basic_Information']
#     t= get()
#     zhihu_col.save(t)
get()
# print()