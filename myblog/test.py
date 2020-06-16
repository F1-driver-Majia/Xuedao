import unittest
from django.test import Client
import requests


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.session_key = '9fd4e6da765480d75ad015a6b3ac002d'


    def test_unlogin(self):
        data = {
            'sub_id': '0',
            'les_id': '1',
            'title': '123',
            'content': '123',
            'Loginid': ''
        }
        res = requests.get(url='http://127.0.0.1:8000/api/upload',params=data)
        print('正在测试未登录状态')
        print(res.status_code,res.text)

    def test_upload(self):
        data = {
            'sub_id': '0',
            'les_id': '1',
            'title': '123',
            'content': '123',
            'Loginid': self.session_key
        }

        res = requests.get(url='http://127.0.0.1:8000/api/upload', params=data)


        print('正在测试正常提交')
        print(res.status_code,res.text)

    def test_uploadfrequent(self):
        data = {
            'sub_id': '0',
            'les_id': '1',
            'title': '123',
            'content': '123',
            'Loginid': self.session_key
        }

        res0 = requests.get(url='http://127.0.0.1:8000/api/upload', params=data)
        res1 = requests.get(url='http://127.0.0.1:8000/api/upload', params=data)

        print('正在测试重复提交')
        print(res1.status_code,res1.text)



if __name__ == '__main__':
    unittest.main()
