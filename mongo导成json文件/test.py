import pymongo
import json

asd = pymongo.MongoClient('172.25.2.60', 27017)

db = asd['Conference_Database']

_table = db['ZJ_yuqing']

with open('张江集团舆情.json', 'a', encoding='utf-8') as f:
    data = list()
    for item in _table.find({}, {'_id': 0}):
        # print('asdsadasd            ', item)
        # asd = item['坐标']
        # lng = str(asd).split(',')[0]
        # lat = str(asd).split(',')[1]
        # # item['lng'] = lng
        # # item['lat'] = lat
        data.append(item)
    f.write(json.dumps(data, ensure_ascii=False))