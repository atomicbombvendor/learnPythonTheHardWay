# coding=utf-8
import cookielib
import gzip
import urllib2
from abc import abstractmethod
from io import BytesIO

from ExoiLogin import LoginExoi
from ExoiTest.LogSingleton import LogSingleton


class AbstractEXOI:

    def __init__(self):
        self.log_exoi = LogSingleton().get_logger()
        self.Login_Cookie = LoginExoi().get_cookie()
        self.cook_file_name = 'cookie_exoi.txt'
        self.content_url = 'http://geexoidevap8002.morningstar.com/' \
                           'DataOutput.aspx?package=%s&Content=%s&IdType=%s' \
                           '&Id=%s&ReportType=%s&Dates=%s'
        self.content = ''
        self.headers = {
            'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'identity;q=1.0,compress;q=0.8,gzip;q=0.5, deflate;q=0.3,*;q=0',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'geexoidevap8002.morningstar.com',
            'Pragma': 'no - cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/58.0'
        }

    # 根据参数获取xml内容，并设置到self.content中
    def get_content(self, param):
        try:
            intact_url = self.construct_url(param)
            cookie = cookielib.LWPCookieJar()
            cookie.load(self.cook_file_name, ignore_discard=False, ignore_expires=False)
            request = urllib2.Request(intact_url, None, self.headers)
            # 需要Header
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            response = opener.open(request)
            content = response.read()  # content是压缩过的数据
            try:
                buff = BytesIO(content)  # 把content转为文件对象, Gzip解压
                f = gzip.GzipFile(fileobj=buff)
                resource = f.read().decode('utf-8')

                # resource = content.decode('GBK')  # 不是gzip的压缩方式

                status = response.getcode()
                if status == 200:
                    self.log_exoi.info(u"获取页面请求成功, url->\n%s" % intact_url)
                else:
                    self.log_exoi.info(u"获取页面请求失败, url->\n%s" % intact_url)
                self.content = resource
            except IOError, e:
                    if e.message.find('gzipped') > 0:
                        resource = content.decode('utf-8')  # 不是gzip的压缩方式
                        status = response.getcode()
                        if status == 200:
                            self.log_exoi.info(u"获取页面请求成功, url->\n%s" % intact_url)
                        else:
                            self.log_exoi.info(u"获取页面请求失败, url->\n%s" % intact_url)
                        self.content = resource
        except urllib2.HTTPError, e:
            self.log_exoi.error(u'The server couldn\'t fulfill the request')
            self.log_exoi.error(u'Error code: ' + e.reason)
        except urllib2.URLError, e:
            self.log_exoi.error(u'We failed to reach a server.')
            self.log_exoi.error(u'Reason: ' + e.reason)

    @abstractmethod
    def check_value(self, line_value): pass

    # 解析line，找出拼接URL需要的参数
    @abstractmethod
    def parse_line(self, line_value): pass
    
    @abstractmethod
    def construct_url(self, param): pass
