import pymongo,charts

conn = pymongo.MongoClient('localhost', 27017)
ganji_db = conn['ganji']
data_collection = ganji_db['data']

#清洗地区数据,只保留地级市
for i in data_collection.find():
    data_collection.update({'_id':i['_id']}, {'$set':{'area':i['area'].split('-')[0]}})

citys = list(set([i['area'] for i in data_collection.find()]))
#找到所有的城市
citys_data = [(i,data_collection.find({'area':i}).count()) for i in citys]
#构造各个城市的对应发帖数量的元组列表
citys_data = sorted(citys_data, key=lambda x:x[1], reverse=True)
#将其排序

#进行柱状图展示前十名的城市
series = [{
    'name':i[0],
    'data':[i[1]],
    'type':'column',
} for i in citys_data[:20] ]
print(series)
charts.plot(series, show='inline')
charts.plot(series, show='inline', options=dict(title=dict(text='武汉赶集网帖子发布地区分布前10')))