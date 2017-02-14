import urllib
from urllib import request
from urllib import parse
from http import cookiejar

import config

class Auth(object):
    
    def __init__(self, username, password):
        opener = request.build_opener(
            request.HTTPCookieProcessor(
                cookiejar.CookieJar()
            )
        )

        if True == config.NET['PROXY']['ENABLE']:
            opener = request.build_opener(
                request.HTTPCookieProcessor(
                    cookiejar.CookieJar()
                ),
                request.ProxyHandler({
                    'http': config.NET['PROXY']['URL'],
                    'https': config.NET['PROXY']['URL'],
                })
            )
        
        request.install_opener(opener)

        self.username = username
        self.password = password

    def sign_in(self):
        url = 'https://wam.inside.nsn.com/siteminderagent/forms/login.fcc'

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,et;q=0.4,zh-TW;q=0.2'
        }

        data = parse.urlencode({
            'SMENC': 'ISO-8859-1', 
            'SMLOCALE': 'US-EN', 
            'USER': self.username, 
            'PASSWORD': self.password, 
            'target': 'https://wam.inside.nsn.com/', 
            'smauthreason': 0,
            "postpreservationdata": ""
        }).encode() 

        req = request.Request(url, data, header)
        resp = request.urlopen(req)

        if -1 != resp.geturl().find('Authentication-error'):
            return False
        return True

    def sign_out(self):
        return True