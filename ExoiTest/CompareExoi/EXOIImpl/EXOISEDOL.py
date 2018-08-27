# coding=utf-8

from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from lxml import etree


class EXOISEDOL(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.value_mapping = {
            1002: 'ExchangeId'
        }

        self.init_url = 'http://geexoidevap8002.morningstar.com/' \
                        'DataOutput.aspx?package=%s&Content=%s&IdType=%s' \
                        '&Id=%s'

    # 检查传入的记录的值可以可以在xml中找到
    def check_value(self, line_value):
        flag = False
        values = self.parse_line_value(line_value)

        # 使用xpath解析xml
        tree2 = etree.XML(self.content.encode('utf-8'))

        # 这里要区分点的类型是
        path = "/ShareClassInfo[@companyId='{companyId}' and @shareClassId='{shareClassId}']/" \
               "{targetNode}='{targetNode_value}'".format(companyId=values['companyId'],
                                                        shareClassId=values['shareClassId'],
                                                        targetNode=values['targetNode'],
                                                        targetNode_value=values.get(values.get('targetNode')))
        target_node = tree2.xpath(path)
        if target_node:
            flag = True

        return flag

    # 把每一行的数据转换为一个字典，方便查询
    def parse_line_value(self, line_value):
        values = {
            'companyId': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['companyId'] = value_set[0]
        values['shareClassId'] = value_set[1]
        values['targetNode'] = self.value_mapping.get(int(value_set[2]))
        values[self.value_mapping.get(int(value_set[2]))] = self.get_value(value_set)

        return values

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = {'Package': 'EquityData',
                 'Content': 'ShareClassInfo',
                 'IdType': 'EquityShareClassId',
                 'Id': ''}

        values = line_value.split("|")
        Id = values[1]
        param['Id'] = Id

        return param

    # 产生完整的URL
    def construct_url(self, param):
        # 把所有的key转换为小写的
        a_lower = {k.lower(): v for k, v in param.items()}
        package = a_lower.get('package'.lower())
        content = a_lower.get('content'.lower())
        Id = a_lower.get('Id'.lower())
        IdType = a_lower.get('IdType'.lower())
        intact_url = self.init_url % (package, content, IdType, Id)
        return intact_url

    def get_value(self, value_set):
        return value_set[3]
