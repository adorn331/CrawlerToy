#调查指定类目七天内发帖量折线图
from datetime import timedelta, date

import pymongo

import charts

conn = pymongo.MongoClient('localhost', 27017)
ganji_db = conn['ganji']
data_collection = ganji_db['sample']

#清洗数据, 更换日期格式,并且只取归类的最后一个
for i in data_collection.find():
    data_collection.update({'_id':i['_id']}, {'$set':{'pub_date':i['pub_date'].replace('.', '-')
                                                     ,'cates':i['cates'][-1]}})

#需要的类目
require = ['北京二手笔记本', '北京二手手机', '北京二手台式机/配件']

#获得一段时间内的全部单日的列表 !!!!
def get_dates(start_date, end_date):
    start = date(*[int(i) for i in start_date.split('-')])
    end = date(*[int(i) for i in end_date.split('-')])
    delta = timedelta(days = 1)
    while(start <= end):
        yield str(start)
        start += delta

#获取需要类目在给定时间内的发帖次数
def get_data_within(start_date, end_date, cates):
    for item in cates:
        item_post = []
        for date in get_dates(start_date, end_date):
            item_post.append(data_collection.find({'cates':item, 'pub_date':date}).count())
        data = {
            'name': item,
            'data': item_post,
            'type': 'line'
        }
        yield data

#作图
options = {
    'chart': {'zoomType':'xy'},
    'title': {'text': '不同类目发帖量统计'},
    'subtitle': {'text': '可视化统计图表'},
    'xAxis': {'categories': [i for i in get_dates('2015-12-25', '2016-1-2')]},
    'yAxis': {'title': {'text': '数量'}}
    }

series = [i for i in get_data_within('2015-12-25', '2016-1-2', require)]

charts.plot(series, options=options, show='inline')
# options=dict(title=dict(text='Charts are AWESOME!!!'))

#手动输入示范效果
# series = [
#     {
#     'name': 'OS X',
#     'data': [11,2,3,4],
#     'type': 'line',
#     'y':5
# }, {
#     'name': 'Ubuntu',
#     'data': [8,5,6,7],
#     'type': 'line',
#     'color':'#ff0066'
# }, {
#     'name': 'Windows',
#     'data': [12,6,7,2],
#     'type': 'line'
# }, {
#     'name': 'Others',
#     'data': [29,24,68,23],
#     'type': 'line'
# }
#          ]


