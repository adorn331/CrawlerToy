import requests
from bs4 import BeautifulSoup

douban_url = 'https://movie.douban.com/top250'
save_path = 'douban_top_250'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

def parser_html(url):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    titles = [i.get_text() for i in soup.select('div.hd > a > span:nth-of-type(1)')]
    scores = [i.get_text() for i in soup.select('span.rating_num')]
    descriptions = [i.get_text() for i in soup.select('span.inq')]
    return ({'title':t, 'score':s, 'description':d}
            for t, s, d in zip(titles, scores, descriptions))

def crawl_pgs(base_url):
    #每一页25个
    for i in range(0, 250, 25):
        yield parser_html(base_url + '?start=' + str(i))

def main():
    with open(save_path, 'w', encoding='utf-8') as f:
        for pg_data in crawl_pgs(douban_url):
            for item in pg_data:
                movie = '%s   %s\n%s\n\n' %(item['title'], item['score'], item['description'])
                print(movie)
                f.write(movie)

if __name__ == '__main__':
    main()