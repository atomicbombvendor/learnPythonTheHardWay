# coding=utf-8
import cookielib
import urllib2
from abc import abstractmethod
from io import BytesIO
import gzip
from ExoiLogin import LoginExoi


class ExoiType:

    def __init__(self):
        self.Login_Cookie = LoginExoi().get_cookie()
        self.cook_file_name = 'cookie_exoi.txt'
        self.content_url = 'http://geexoidevap8002.morningstar.com/' \
                           'DataOutput.aspx?package=%s&Content=%s&IdType=%s' \
                           '&Id=%s&Dates=%s'
        self.content = ''
        self.value_mapping = {
        46000: 'OwnerName',
        46001: 'IsCurrent',
        46002: 'HoldingType',
        46003: 'HoldingDescription',
        46004: 'TransactionDate',
        46005: 'NumberOfShares',
        46006: 'SharesOwnedPostTransactionPercentage',
        46007: 'TransactionType',
        46008: 'TransactionShares',
        46009: 'TransactionPrice',
        46010: 'TransactionPercentage',
        46011: 'TransactionValue',
        46012: 'FilingDate',
        46013: 'NotificationDate',
        46014: 'NewReport',
        46015: 'IsExHolding'}
        self.headers = {
            'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
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
            # 把所有的key转换为小写的
            a_lower = {k.lower(): v for k, v in param.items()}
            package = a_lower.get('package'.lower())
            content = a_lower.get('content'.lower())
            Id = a_lower.get('Id'.lower())
            IdType = a_lower.get('IdType'.lower())
            ReportType = a_lower.get('ReportType'.lower())
            Dates = a_lower.get('Dates'.lower())

            url_param = self.content_url % (package, content, IdType, Id, Dates)
            cookie = cookielib.LWPCookieJar()
            cookie.load(self.cook_file_name, ignore_discard=True, ignore_expires=True)
            request = urllib2.Request(url_param, None, self.headers)
            # 需要Header
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            response = opener.open(request)
            content = response.read()  # content是压缩过的数据

            buff = BytesIO(content)  # 把content转为文件对象
            f = gzip.GzipFile(fileobj=buff)
            resource = f.read().decode('utf-8')
            status = response.getcode()
            if status == 200:
                print u"获取请求成功, url->\n%s" % url_param
            else:
                print u"获取请求失败, url->\n%s" % url_param
            self.content = resource
        except urllib2.HTTPError, e:
            print u'The server couldn\'t fulfill the request'
            print u'Error code: ', e.reason
        except urllib2.URLError, e:
            print u'We failed to reach a server.'
            print u'Reason: ', e.reason

    @abstractmethod
    def check_value(self, line_value): pass
