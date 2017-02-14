import urllib
import ssl
from urllib import request
from urllib import parse
from http import cookiejar
from bs4 import BeautifulSoup

from config import NET
        
ssl._create_default_https_context = ssl._create_unverified_context  

class Spider(object):

    def __init__(self, username, password):
        opener = request.build_opener(
            request.HTTPCookieProcessor(
                cookiejar.CookieJar()
            )
        )

        if True == NET['PROXY']['ENABLE']:
            opener = request.build_opener(
                request.HTTPCookieProcessor(
                    cookiejar.CookieJar()
                ),
                request.ProxyHandler({
                    'http': NET['PROXY']['URL'],
                    'https': NET['PROXY']['URL'],
                })
            )
        
        request.install_opener(opener)

        self.username = username
        self.password = password
    
    def get_page(self, url, in_nokia=True):
        if in_nokia:
            auth = "https://wam.inside.nsn.com/siteminderagent/forms/login.fcc"

            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,et;q=0.4,zh-TW;q=0.2"
            }

            data = parse.urlencode({
                "SMENC": "ISO-8859-1", 
                "SMLOCALE": "US-EN", 
                "USER": self.username, 
                "PASSWORD": self.password, 
                "target": url, 
                "smauthreason": 0, 
                "postpreservationdata": ""
            }).encode()

            req = request.Request(auth, data, header)
            html = request.urlopen(req).read()
            return html
        else:
            html = request.urlopen(url).read()
            return html

    def get_soup(self, html=None):
        src = self.driver.page_source if None == html else html
        soup = BeautifulSoup(src, 'html.parser')
        return soup

    def get_param(self, url):
        parser = urlparse.urlparse(url)
        param = urlparse.parse_qs(parser.query)
        return param