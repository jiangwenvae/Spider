from urllib.parse import urlencode
import requests
base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/u/1251000504',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}

def get_page(since_id=None):
    params={
        'type':'uid',
        'value':'1251000504',
        'containerid':'1076031251000504',
        'since_id':since_id
    }
    url = base_url+urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            json = response.json()
            items = json.get('data').get('cardlistInfo')
            next_since_id = items['since_id']
            return (json, next_since_id)
    except requests.ConnectionError as e:
        print('Error',e.args)

from pyquery import PyQuery as pq

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            try:
                if pq(item.get('text')).text() == None:
                    continue
            except:
                continue
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield  weibo

from pymongo import MongoClient

client = MongoClient()
db = client['weibo']
collection = db['weibo']
def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')

if __name__=='__main__':
    for page in range(10):
        if page == 0:
            print("第{}页".format(page + 1))
            tuple_since_id = get_page()
            results = parse_page(tuple_since_id[0])
            for result in results:
                save_to_mongo(result)
                print(result)
        else:
            print("第{}页".format(page + 1))
            tuple_since_id = get_page(tuple_since_id[1])
            results = parse_page(tuple_since_id[0])
            for result in results:
                save_to_mongo(result)
                print(result)
