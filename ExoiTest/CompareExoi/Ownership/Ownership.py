# coding=utf-8
import gzip
import httplib
import urllib2
from io import BytesIO

from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from ExoiTest.CompareExoi.IssueIdMap import IssueId


class Ownership(AbstractEXOI):

    def construct_url(self, param):
        issue_id = "E0USA00834"
        issue_id_part = "%s/institution/summary"
        return (self.init_url + issue_id_part % issue_id).encode("utf-8")

    def parse_line(self, line_value):
        pass

    def check_value(self, line_value):
        pass

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.issueId = IssueId()
        self.init_url = 'https://api-stg.morningstar.com/dataapi/v2/ownership/v2/'

        self.content = ''

        self.headers = {
            'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'application/gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no - cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'ApiKey': 'pXc8z2UFct5ARW3ZxYlS58UG7VgeO5W9',
            'X-API-UserId': 'B337B227-0DF4-4D08-B548-BDE8F381C9E0',
            'X-API-ProductId': 'EqutiyAPI'
        }

    # 根据参数获取xml内容，并设置到self.content中
    def get_content(self, param):
        intact_url = self.construct_url(param)
        try:
            request = urllib2.Request(intact_url, None, self.headers)
            response = urllib2.urlopen(request, timeout=10)
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
            self.log_exoi.error(u'The server could n\'t fulfill the request\n' + intact_url)
            self.log_exoi.error(u'Error code: ' + e.reason)
            self.content = ''
        except urllib2.URLError, e:
            self.log_exoi.error(u'We failed to reach a server\n' + intact_url)
            self.log_exoi.error(u'Reason: ' + e.reason)
            self.content = ''
        except httplib.BadStatusLine, e:
            self.log_exoi.error(u'We failed to reach a server\n' + intact_url)
            self.log_exoi.error(u'Reason: ' + e.message)
            self.content = ''
