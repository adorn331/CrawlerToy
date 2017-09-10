from main import url_collection, data_collection
import time

#监控数据库中获取数据情况
def monitor():
    while True:
        print('%d url fetched.' % url_collection.find().count())
        print('%d detail data fetched.' % data_collection.find().count())
        time.sleep(10)   #10秒监控一下获取数据情况

monitor()
