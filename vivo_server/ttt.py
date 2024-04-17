import requests
import base64
from auth_util import gen_sign_headers

APP_ID = '3038003586'
APP_KEY = 'AyzUmxrvZsnoYCyy'
URI = '/ocr/general_recognition'
METHOD = 'POST'
DOMAIN = 'api-ai.vivo.com.cn'
PIC_FILE = 'test.png'


def ocr_test():
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
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code, response.text)


if __name__ == '__main__':
    ocr_test()
