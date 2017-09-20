#统计北京某个区各种类目前三名的柱状图
import pymongo
import charts

conn = pymongo.MongoClient('localhost', 27017)
ganji_db = conn['ganji']
data_collection = ganji_db['sample']

areas = list(set(i['area'][0] for i in data_collection.find() if i['area']))
print(areas)   #查看所有区,选一个柱状图

area = '朝阳' #选中了朝阳区,画图
pipeline = [
    {'$match':{ 'area' :area}},   #area只要在'area'这个list数据项里面就会被match
    {'$group':{'_id':'$cates', 'counts':{'$sum':1}}},
                                #'avg_price':{'$avg':'$price'}  除了实现统计个数还可以取它另一个字段的平均值
    {'$sort':{'counts':-1}},
    {'$limit':3}
]

# for i in data_collection.aggregate(pipeline):
#     print(i)

series = [{
    'name': i['_id'],
    'data':[i['counts']],
    'type':'column'
} for i in data_collection.aggregate(pipeline)]

charts.plot(series, show='inline')