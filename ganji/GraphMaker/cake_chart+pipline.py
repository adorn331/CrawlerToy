#使用pipline在查询数据的时候就进行分类统计,而不使用Python查询Python统计
#画个饼图

import pymongo

from GraphMaker import charts

conn = pymongo.MongoClient('localhost', 27017)
ganji_db = conn['ganji']
data_collection = ganji_db['sample']

def pipline_on_date(date):
    pipline = [
        {'$match':{'pub_date':date}},
                #:{'$and':{'age':18, 'name':chuige'}} 符合两个条件的时候

        {'$group':{'_id':'$cates', 'counts':{'$sum' : 1}}}, #分组,然后计算每一组数据
        #'_id':{'$slice':['$cates',2,1]} 如果是取cates[2]作为分组依据的话,2代表起始位置,1代表个数

        {'$sort':{'counts':-1}},#根据分组然后排序分组

        {'$limit':10}#最多显示10个
    ]
    return pipline



options = {
    'chart'   : {'zoomType':'xy'},
    'title'   : {'text': '发帖量统计'},
    'subtitle': {'text': '可视化统计图表'},
    }
series =  [{
    'type': 'pie',
    'name': 'pie charts',
    'data':[[i['_id'], i['counts']] for i in data_collection.aggregate(pipline_on_date('2015-12-24'))]

        }]

charts.plot(series, options=options, show='inline')
#手动输入效果
# series =  [{
#     'type': 'pie',
#     'name': 'Browser share',
#     'data':[
#             ['北京二手家电', 8836],
#             ['北京二手文体/户外/乐器', 5337],
#             ['北京二手数码产品', 4405],
#             ['北京二手服装/鞋帽/箱包', 4074],
#             ['北京二手母婴/儿童用品', 3124],
#             ['北京二手台式机/配件', 2863],
#             ['北京二手图书/音像/软件', 2777],
#             ['北京二手办公用品/设备', 2496],
#             ['北京二手家具', 1903],
#             ['北京二手美容/保健', 1838],
#             ['北京二手手机', 1603],
#             ['北京二手笔记本', 1174],
#             ['北京二手设备', 1004],
#             ['北京其他二手物品', 761],
#             ['北京二手平板电脑', 724]
#             ]
#
#         }]

