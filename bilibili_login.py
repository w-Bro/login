import requests
import binascii
import rsa
import random
import time
import json
from config import bi_password, bi_username

class Bilibili(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.login_url = 'https://passport.bilibili.com'
        self.validate_url = 'https://api.geetest.com'

    def login(self):
        login_params = {}
        try:
            print('获取登录必要参数 gt、challenge、key...')
            url = self.login_url + '/web/captcha/combine?plat=6'
            response = self.session.get(url, headers=self.headers).json()
            if response['code'] == 0:
                keys = ['gt', 'challenge', 'key']
                [login_params.setdefault(key, response['data']['result'][key]) for key in keys]
        except Exception as e:
            print('获取登录参数步骤失败', str(e))
            return False

        try:
            # url = self.validate_url + '/get.php'
            # params = {
            #     'is_next': True,
            #     'type': 'click',
            #     'gt': login_params['gt'],
            #     'challenge': login_params['challenge'],
            #     'lang': 'zh-cn',
            #     'https': False,
            #     'protocol': 'https://',
            #     'offline': False,
            #     'product': 'embed',
            #     'api_server': 'api.geetest.com',
            #     'isPC': True,
            #     'area': '#geetest-wrap',
            #     'width': '100%',
            #     'callback': 'geetest_' + str(int(time.time() * 1000))
            # }
            #
            # response = self.session.get(url, params=params, headers=self.headers)
            # api GITHUB地址 https://github.com/zhiying8710/geetest_crack
            print('使用api识别验证码...')
            url = 'http://47.94.91.142:8081/avc/demo/v'
            data = {
                "model": "gt",
                "data": {
                    "gt": login_params['gt'],
                    "challenge": login_params['challenge'],
                    "type": "gt3",
                    "referer": self.login_url + '/web/captcha/combine?plat=6'
                }

            }
            response = self.session.post(url, data=json.dumps(data), headers={'Content-type': 'application/json'})
            if response.json()['success']:
                validate = response.json()['data']['valid']
            else:
                raise Exception("文字点选验证码识别失败")
        except Exception as e:
            print(str(e))
            return False

        try:
            print('进行密码加密...')
            url = self.login_url + '/login'
            r = random.random()
            data = {'act': 'getkey', 'r': str(r)}
            response = self.session.get(url, headers=self.headers, params=data)
            encrypt_password = self.rsa_encrypt(self.password, response.json()['hash'], response.json()['key'])
            login_params.setdefault('password', encrypt_password)
            login_params.setdefault('username', self.username)
        except Exception as e:
            print('密码加密步骤失败', str(e))
            return False

        try:
            print('进行登录...')
            login_params.setdefault('captchaType', 6)
            login_params.setdefault('goUrl', 'https://www.bilibili.com/')
            login_params.setdefault('keep', True)
            login_params.setdefault('validate', validate)
            login_params.setdefault('seccode', validate + '|jordan')
            # print(login_params)

            url = self.login_url + '/web/login/v2'
            response = self.session.post(url, data=login_params, headers=self.headers)
            if response.json()['code'] == 0:
                print('登录成功')
                return True
            else:
                raise Exception("code is not 0")
        except Exception as e:
            print("登录失败", str(e))
            return False

    @staticmethod
    def rsa_encrypt(password, hash, key):
        """
        rsa加密
        :param password:
        :param hash:
        :param key:
        :return:
        """
        pw = str(hash + password).encode('utf8')
        key = rsa.PublicKey.load_pkcs1_openssl_pem(key)
        pw = rsa.encrypt(pw, key)
        password = binascii.b2a_base64(pw)

        return password


if __name__ == '__main__':
    bili = Bilibili(bi_username, bi_password)
    if bili.login():
        pass