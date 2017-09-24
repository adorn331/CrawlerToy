from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests, pymongo,time, random, threading

###从http://cn-proxy.com/获取几个较好的代理切换使用
proxy_list = [
    '101.200.45.131:3128',
    '121.40.199.105:80',
    '120.25.211.80:9999',
    '114.215.102.168:8081'
]

proxies_ip = random.choice(proxy_list)
proxies = {'http' : proxies_ip}

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Connection':'keep-active'
}


#获取所有二手商品频道
def get_channels():
    url_host = 'http://wh.ganji.com'
    web_data = requests.get(url_host + '/wu', headers=headers, proxies=proxies)
    soup = BeautifulSoup(web_data.text, 'lxml')
    channels = [url_host + i.get('href') for i in soup.select('#wrapper div.main dd a')]
    return channels

#获取某个二手商品频道的某个页面下的所有url
def get_pg_urls(url):
    #time.sleep(random.randint(1,3))
    try:
        web_data = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(web_data.text, 'lxml')
        if len(soup.select('div.noinfo')) != 0:
            print('fail to get this page...')
            pass       #页数超过, 没有商品信息
        else:
            all_tags = soup.select('td.t a.t')
            tags = filter(lambda x: len(x.find_all('span')) == 0, all_tags) #筛去带有"精"标签的广告帖
            urls = [i.get('href').split('?')[0] for i in tags]
            for i in urls:
                print(i)
                url_collection.insert_one({'url' : i})
    except:
        print('爬取页面信息失败')

#获取某个频道下所有的url, 默认最多为70页
def get_channel_urls(channel_url, pg_num=70):
    for i in range(1, pg_num + 1):
        # time.sleep(random.randint(1, 3))
        get_pg_urls(channel_url + 'o' + str(i))
    print('done the channel:%s' % (channel_url,))

#获取某个详情帖子的信息
def get_detail_data(url):
    try:
        web_data = requests.get(url,  headers=headers, proxies=proxies)
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
    except:
        print('获取详情数据失败')


conn = pymongo.MongoClient('localhost', 27017)
ganji_db = conn['ganji']
url_collection = ganji_db['url']
data_collection = ganji_db['data']

if __name__ == '__main__':
    url_pool = Pool()
    data_pool = Pool()

    channels = get_channels()
    print(channels)
    url_pool.map(get_channel_urls, channels)    #先获取所有的详情页url

    data_pool.map(get_detail_data, [i['url'] for i in url_collection.find()])
    #根据获取的url逐一获取信息

