from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests, pymongo,time, random, threading

channels_count = 0

#获取所有二手商品频道
def get_channels():
    url_host = 'http://wh.ganji.com'
    web_data = requests.get(url_host + '/wu')
    soup = BeautifulSoup(web_data.text, 'lxml')
    channels = [url_host + i.get('href') for i in soup.select('#wrapper div.main dd a')]
    return channels

#获取某个二手商品频道的某个页面下的所有url
def get_pg_urls(url):
    time.sleep(random.randint(1,3))
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    if len(soup.select('div.noinfo')) != 0:
        print('fail to get this page...')
        pass       #页数超过, 没有商品信息
    else:
        all_tags = soup.select('td.t a.t')
        tags = filter(lambda x: len(x.find_all('span')) == 0, all_tags) #筛去带有"精"标签的广告帖
        urls = [i.get('href').split('?')[0] for i in tags]
        for i in urls:
            url_collection.insert_one({'url' : i})

#获取某个频道下所有的url, 默认最多为100页
def get_channel_urls(channel_url, pg_num=100):
    global channels_count
    for i in range(1, pg_num + 1):
        time.sleep(random.randint(1, 3))
        get_pg_urls(channel_url + 'o' + str(i))
    channels_count += 1
    print('done :%s the %dth channel' % (channel_url, channels_count))

#获取某个详情帖子的信息
def get_detail_data(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')

    title = soup.select('h1.info_titile')[0].get_text()
    price = soup.select('span.price_now > i')[0].get_text()
    area = soup.select('div.palce_li i')[0].get_text()
    views = int(soup.select('span.look_time')[0].get_text()[:-3])

    data_collection.insert_one({
        'title':title,
        'price':price,
        'area':area,
        'views':views
    })

#没两秒监控获取数据情况
def counter():
    while True:
        print('%d url fetched.' % url_collection.find().count())
        print('%d detail data fetched.' % data_collection.find().count())
        time.sleep(2)


conn = pymongo.MongoClient('localhost', 27017)
ganji_db = conn['ganji']
url_collection = ganji_db['url']
data_collection = ganji_db['data']

if __name__ == '__main__':
    spy = threading.Thread(target=counter, daemon=True)
    spy.start()

    url_pool = Pool()
    data_pool = Pool()

    channels = get_channels()
    url_pool.map(get_channel_urls, channels)

    data_pool.map(get_detail_data, [i['url'] for i in url_collection.find()])
