import requests
from urllib.parse import urlencode,quote,unquote

headers = {
    'Host': 'so.toutiao.com',

    'Referer': 'https://so.toutiao.com/search?keyword=%E8%A1%97%E6%8B%8D&pd=atlas&dvpf=pc&aid=4916&page_num=0&search_json={%22from_search_id%22:%222022040316335201021218304330C35A48%22,%22origin_keyword%22:%22%E8%A1%97%E6%8B%8D%22,%22image_keyword%22:%22%E8%A1%97%E6%8B%8D%22}',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',

    'X-Requested-With': 'XMLHttpRequest',

    'Cookie': 'passport_csrf_token=92a1b4e0108fb8384f5b81554b5b5424; tt_webid=7053044990251386398; _S_DPR=1.25; _S_IPAD=0; MONITOR_WEB_ID=7053044990251386398; ttwid=1%7CoqMwjUw5WGRdjYizT8quhnfpAchk3v_E3YLa1riJgrY%7C1648972603%7Cbaea5aebf3461426baaede977fa55b0efec3033a9f0d6a3e26684ba80f607ee9; _S_WIN_WH=1536_722'

}

def get_page(page_num):
    params = {
        'keyword':unquote('%E8%A1%97%E6%8B%8D') ,
        'pd':'atlas',
        'dvpf':'pc',
        'aid': '4916' ,
        'page_num':page_num,
        'search_json':{"from_search_id":"2022040316335201021218304330C35A48","origin_keyword":"街拍","image_keyword":"街拍"},
        'rawJSON':'1',
        'search_id':'2022040317334901015013503043241DAC'
    }
    url = 'https://so.toutiao.com/search/?'+urlencode(params,headers)
    try:
        response = requests.get(url,headers=headers,params=params)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('rawData'):
        images = json.get('rawData').get('data')
        for image in images:
            link = image.get('img_url')
            yield {
                    'image':image.get('img_url'),
                    'title':"街拍",
                    'text':image.get('text')
                }

import os
from hashlib import md5

def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print("Already Downloaded",file_path)
    except requests.ConnectionError:
        print('Failed to Save image')

from multiprocessing.pool import Pool

def main(page_num):
    json = get_page(page_num)
    for item in get_images(json):
        print(item)
        save_image(item)

GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    # pool = Pool()
    # groups = ([x*20 for x in range(GROUP_START,GROUP_END+1)])  #使用这种方式启动出现bug，原因还没有找到
    # pool.map(main,groups)
    # pool.close()
    # pool.join()
    for i in range(1,10):
        main(i)
