from main import url_collection, data_collection
import time, datetime

#监控数据库中获取数据情况
def monitor():
    while True:
        print('time:', datetime.datetime.now())
        print('%d url fetched.' % url_collection.find().count())
        print('%d detail data fetched.' % data_collection.find().count())
        print('-' * 30)
        time.sleep(20)   #20秒监控一下获取数据情况

monitor()
