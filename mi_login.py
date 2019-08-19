import requests
import hashlib
import time
import config


class Mi(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
    
    def login(self):
        url = f'https://account.xiaomi.com/pass/serviceLoginAuth2?_dc={time.time() * 1000}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'https://account.xiaomi.com/pass/serviceLogin?callback=https%3A%2F%2Forder.mi.com%2Flogin%2Fcallback%3Ffollowup%3Dhttps%253A%252F%252Fwww.mi.com%252F%26sign%3DNzY3MDk1YzczNmUwMGM4ODAxOWE0NjRiNTU5ZGQyMzFhYjFmOGU0Nw%2C%2C&sid=mi_eshop&_bannerBiz=mistore&_qrsize=180'
        }
        # 对密码进行MD5加密
        md5 = hashlib.md5()
        md5.update(self.password.encode('utf8'))
        data = {
            '_json': 'true',
            '_sign': 'KIoyNE+yRQmbP3xYn1eGTWJt4EE=',
            'callback': 'https://order.mi.com/login/callback?followup=https%3A%2F%2Fwww.mi.com%2F&sign=NzY3MDk1YzczNmUwMGM4ODAxOWE0NjRiNTU5ZGQyMzFhYjFmOGU0Nw,,',
            'cc': '',
            # 大写
            'hash': md5.hexdigest().upper(),
            'qs': '%3Fcallback%3Dhttps%253A%252F%252Forder.mi.com%252Flogin%252Fcallback%253Ffollowup%253Dhttps%25253A%25252F%25252Fwww.mi.com%25252F%2526sign%253DNzY3MDk1YzczNmUwMGM4ODAxOWE0NjRiNTU5ZGQyMzFhYjFmOGU0Nw%252C%252C%26sid%3Dmi_eshop%26_bannerBiz%3Dmistore%26_qrsize%3D180',
            'serviceParam': '{"checkSafePhone":false}',
            'sid': 'mi_eshop',
            'user': self.username
        }
        
        response = self.session.post(url, data=data, headers=headers)
        if '成功' in response.text:
            print('小米官网登录成功')
            
            url = 'https://api2.order.mi.com/flashsale/getslideshow?callback=__jp0'
            response = self.session.get(url)
            print(response.text)
    
        
if __name__ == '__main__':
    mi = Mi(config.mi_username, config.mi_password)
    mi.login()