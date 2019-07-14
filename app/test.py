import unittest
#!/usr/bin/python
#encoding:utf-8
from app import app
import requests

class TestPost(unittest.TestCase):
    def test_post(self):

        self.test_app = app.test_client()

        response = self.test_app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


import json
import http.client
def base64(file):
    # image转base64
    import base64
    with open(file, "rb") as f:  # 转为二进制格式
        base64_data = base64.b64encode(f.read())  # 使用base64进行加密
        return str(base64_data)

def post_test():
    payload = '[{"uuid":"123123123","imagebase64":"%s","ip":"192.187.980"},{"uuid":"123123123","imagebase64":"%s","ip":"192.187.880"}]'%( base64("02.jpg"),base64("3.jpg"))
    r = requests.post('http://localhost/imageprocess',data=payload)
    print(r.text)

if __name__ == '__main__':
    # 下面替换成您的数据
    post_test()
