# encoding: utf-8
import uuid
import time
import requests
from auth_util import gen_sign_headers
import base64

# 请替换APP_ID、APP_KEY
APP_ID = '3038003586'
APP_KEY = 'AyzUmxrvZsnoYCyy'
URI = '/ocr/general_recognition'
METHOD = 'POST'
DOMAIN = 'api-ai.vivo.com.cn'


URI2 = '/vivogpt/completions'

# 请注意替换APP_ID、APP_KEY

URI3 = '/search/geo'
METHOD3 = 'GET'


def geocode_poi():
    """ 地理编码（poi搜索） """
    params = {
        'keywords': '卓悦汇',
        'city': '深圳',
        'page_num': 2,
        'page_size': 3
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD3, URI3, params)
    print('headers:', headers)
    url = 'http://{}{}'.format(DOMAIN, URI3)
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        data = response.text
    print(data)


def ocr_test(file_name):
    PIC_FILE = file_name
    picture = PIC_FILE
    with open(picture, "rb") as f:
        b_image = f.read()
    image = base64.b64encode(b_image).decode("utf-8")
    post_data = {"image": image, "pos": 2,
                 "businessid": "1990173156ceb8a09eee80c293135279"}
    params = {}
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)

    url = 'http://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, data=post_data, headers=headers)
    content = ""
    if response.status_code == 200:
        x = (response.json())
        for i in x['result']['OCR']:
            print(i['words'])
            content += i['words']
            # for i in x:
            #     print()
    else:
        print(response.status_code, response.text)
    # print(response)
    return content


def sync_vivogpt(content):
    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])

    data = {
        'prompt': '我在餐厅吃饭，这是菜单的一些内容，请帮我推荐一些搭配, 顺便给我介绍这些菜品的历史故事和特点'+content,
        'model': 'vivo-BlueLM-TB',
        'sessionId': str(uuid.uuid4()),
        'extra': {
            'temperature': 0.9
        }
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI2, params)
    headers['Content-Type'] = 'application/json'

    start_time = time.time()
    url = 'https://{}{}'.format(DOMAIN, URI2)
    response = requests.post(
        url, json=data, headers=headers, params=params, stream=True)

    if response.status_code == 200:
        res_obj = response.json()
        print(f'response:{res_obj}')
        if res_obj['code'] == 0 and res_obj.get('data'):
            content = res_obj['data']['content']
            print(f'final content:\n{content}')
    else:
        print(response.status_code, response.text)
    end_time = time.time()
    timecost = end_time - start_time
    print('请求耗时: %.2f秒' % timecost)


if __name__ == '__main__':
    content = ocr_test('./test.png')
    sync_vivogpt(content)
    # geocode_poi()
