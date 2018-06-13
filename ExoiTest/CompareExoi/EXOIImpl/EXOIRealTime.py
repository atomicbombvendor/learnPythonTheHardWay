# coding=utf-8
import gzip
import urllib2
from io import BytesIO

from lxml import etree

from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI


class EXOIRealTime(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.value_mapping = {
                   1029: '@marketDataIdentifier'
        }

        self.init_url = 'http://idservice.morningstar.com/v2/securities/ids-mapping?' \
                        'q=%s&d=AC005,AC003,AC001'

    def get_content(self, param):
        try:
            intact_url = self.construct_url(param)
            request = urllib2.Request(intact_url)
            opener = urllib2.build_opener()
            response = opener.open(request)
            content = response.read()  # content是压缩过的数据
            try:
                buff = BytesIO(content)  # 把content转为文件对象, Gzip解压
                f = gzip.GzipFile(fileobj=buff)
                resource = f.read().decode('utf-8')
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
        except Exception, e:
            self.log_exoi.error(u'Some thing wrong.')
            self.log_exoi.error(u'Reason: ' + e.message)

    # 检查传入的记录的值可以可以在xml中找到
    def check_value(self, line_value):
        flag = False
        values = self.parse_line_value(line_value)

        # 使用xpath解析xml
        tree2 = etree.XML(self.content.encode('utf-8'))

        # 如果DataId节点不存在
        if values['targetNode'] is None:
            self.log_exoi.error("没有找到与%s对应的节点名" % line_value.split('|')[1])
            return

        if '1029' == values['dataId']:
            check_path = "/root/result[@msg='success']"
            check_path_node = tree2.xpath(check_path)
            if len(check_path_node) > 0:
                path_ac005 = "/root/m[@k='" + values['shareClassId'] + "']/r/dv[@d='AC005']"
                path_ac003 = "/root/m[@k='" + values['shareClassId'] + "']/r/dv[@d='AC003']"
                path_ac001 = "/root/m[@k='" + values['shareClassId'] + "']/r/dv[@d='AC001']"
                val_ac005 = tree2.xpath(path_ac005)[0].attrib['v']
                val_ac003 = tree2.xpath(path_ac003)[0].get('v')
                val_ac001 = tree2.xpath(path_ac001)[0].attrib['v']
                val_1029 = "%s.%s.%s" % (val_ac005, val_ac003, val_ac001)
                if values['value'] == val_1029:
                    flag = True

        return flag

    # 把每一行的数据转换为一个字典，方便查询
    def parse_line_value(self, line_value):
        values = {
            'companyId': '',
            'shareClassId': '',
            'dataId': '',
            'value': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['companyId'] = value_set[0]
        values['shareClassId'] = value_set[1]
        values['dataId'] = value_set[2]
        values['value'] = value_set[3]
        values['targetNode'] = self.value_mapping.get(int(value_set[2]))

        return values

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = {}
        values = line_value.split("|")
        Id = values[1]
        param['Id'] = Id
        return param

    # 产生完整的URL
    def construct_url(self, param):
        # 把所有的key转换为小写的
        a_lower = {k.lower(): v for k, v in param.items()}
        Id = a_lower.get('Id'.lower())
        intact_url = self.init_url % (Id)
        return intact_url