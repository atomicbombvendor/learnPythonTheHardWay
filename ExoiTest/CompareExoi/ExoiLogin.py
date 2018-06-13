# coding=utf-8
import cookielib
import urllib
import urllib2

from ExoiTest.LogSingleton import LogSingleton


class LoginExoi:

    def __init__(self):
        self.log_exoi = LogSingleton().get_logger()
        self.login_url = 'http://gehomedevap8005.morningstar.com/login/login.aspx?RT=aHR0cDovL2dlZXhvaWRldmFwODAwMi5tb3JuaW5nc3Rhci5jb20vRGF0YU91dHB1dC5hc3B4P3BhY2thZ2U9RXF1aXR5RGF0YSZDb250ZW50PUZ1bmRhbWVudGFsJklkPTBDMDAwMDBBV1cmSWRUeXBlPUVxdWl0eUNvbXBhbnlJZCZSZXBvcnRUeXBlPVImRGF0ZXM9MjAxMQ=='
        self.cook_file_name = 'cookie_exoi.txt'
        self.login_headers = {
            'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Content-Length': '396',
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'gehomedevap8005.morningstar.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/58.0'
        }

        self.post = {
            '__EVENTVALIDATION': '/wEWBAL+2LvHCwLB2tiHDgK1qbSRCwKC3IeGDMlPgDAobAt3ZlZFDYLORW+tFlpF',
            '__VIEWSTATE': '/wEPDwUJNjAxMDUyNzkyD2QWAgIBD2QWBAIFDw8WAh4LTmF2aWdhdGVVcmwFJ2h0dHA6Ly9nZWhvbWVkZXZhcDgwMDUubW9ybmluZ3N0YXIuY29tL2RkAgYPDxYCHwAFJ2h0dHA6Ly9nZWV4b2lkZXZhcDgwMDIubW9ybmluZ3N0YXIuY29tL2RkZN3bIBl44DML36+Qjsd82OamEtID',
            'btnLogin': 'Login',
            'txtPassword': 'Eq800101',
            'txtUser': 'GlobalEquityData@morningstar.com'
        }

        self.post_data = urllib.urlencode(self.post)
        self.cookie = cookielib.LWPCookieJar(self.cook_file_name)
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookie_handler, urllib2.HTTPHandler)

    # 登录Exoi,获取Cookie,存储Cookie.
    def get_cookie(self):
        # 第一次登录获取验证码尝试，构建request
        request = urllib2.Request(self.login_url, self.post_data, self.login_headers)
        # 得到第一次登录尝试的相应
        response = self.opener.open(request)
        # # 获取其中的内容
        # content = response.read().decode('utf-8')
        # 获取状态吗
        status = response.getcode()
        self.cookie.save(ignore_discard=False, ignore_expires=False)
        if status == 200:
           self.log_exoi.info(u"登录成功")
           self.log_exoi.info(str(self.cookie) + '\n')
        else:
            self.log_exoi.info(u"登录失败\n")