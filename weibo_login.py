import requests
import config


class WeiBo(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        
    def login(self):
        url = 'https://passport.weibo.cn/sso/login'
        data = {
            'client_id': '',
            'code': '',
            'ec': '0',
            'entry': 'mweibo',
            'hff': '',
            'hfp': '',
            'loginfrom': '',
            'mainpageflag': '1',
            'pagerefer': 'https://m.weibo.cn/',
            'password': self.password,
            'qq': '',
            'r': 'https://m.weibo.cn/',
            'savestate': '1',
            'username': self.username,
            'wentry': ''
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F'
        }
        response = self.session.post(url, data=data, headers=headers)
        if response.json()['retcode'] == 20000000:
            print('微博登录成功')
        
            print('---开始获取首页100条微博---')
            url = 'https://m.weibo.cn/feed/friends?'
            response = self.session.get(url)
            results = []
            results += (response.json()['data']['statuses'])
            for i in range(4):
                response = self.session.get(url + 'max_id=' + results[-1]['id'])
                results += (response.json()['data']['statuses'])
            
            print('实际获取微博数量:', len(results))
            for result in results:
                # 打印博主名称，微博内容
                print(result['user']['screen_name'], result['text'])
        
        
if __name__ == '__main__':
    weibo = WeiBo(config.weibo_username, config.weibo_password)
    weibo.login()