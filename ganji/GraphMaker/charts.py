#各个地区总帖子数前20名柱状图
import pymongo

conn = pymongo.MongoClient('localhost', 27017)
ganji_db = conn['ganji']
data_collection = ganji_db['data']

#清洗地区数据,只保留地级市
for i in data_collection.find():
    data_collection.update({'_id':i['_id']}, {'$set':{'area':i['area'].split('-')[0]}})


########以下部分可以使用pipline轻松解决,速度更快
citys = list(set([i['area'] for i in data_collection.find()]))
#找到所有的城市
citys_data = [(i,data_collection.find({'area':i}).count()) for i in citys]
#构造各个城市的对应发帖数量的元组列表
citys_data = sorted(citys_data, key=lambda x:x[1], reverse=True)
#将其排序
#######


#进行柱状图展示前十名的城市
series = [{
    'name':i[0],
    'data':[i[1]],
    'type':'column',
} for i in citys_data[:20] ]

#charts.plot(series, show='inline')
charts.plot(series, show='inline', options=dict(title=dict(text='武汉赶集网帖子发布地区分布前10')))



for i in data_collection.find({'area':'北京'}, {'cates':1, '_id':0, 'pub_date':1}).limit(300):
    print(i)
    #find的参数:第一个字典是查找,第二个是显示的数据项,0代表不显示

#手动输入效果
# series = [
#     {
#     'name': 'OS X',
#     'data': [11],
#     'type': 'column'
# }, {
#     'name': 'Ubuntu',
#     'data': [8],
#     'type': 'column',
#     'color':'#ff0066'
# }, {
#     'name': 'Windows',
#     'data': [12],
#     'type': 'column'
# }, {
#     'name': 'Others',
#     'data': [29],
#     'type': 'column'
# }
#          ]