# coding=utf-8
from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from lxml import etree
import time


class EXOIMergerAndAcquisition(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.value_mapping = {
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
        path = "/MergerAndAcquisitions/MergerAndAcquisition[AcquirerCompanyId='"+values['AcquirerCompanyId'] \
               + "' and TargetCompanyId='"+values['TargetCompanyId']+"']"
        target_node = tree2.xpath(path)

        for node in target_node:
            if self.check_MergerAndAcquisition(node, values):
                flag = True

        return flag

    # 把每一行的数据转换为一个字典，方便查询
    def parse_line_value(self, line_value):
        values = {
            'AcquirerCompanyId': '',
            'TargetCompanyId': '',
            'ExcludingDate': '',
            'Note': '',
            'CashPerShare': '',  # 如果是 3M,则是3;如果是1Y,则是12
            'CashPerShareCurrency': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['AcquirerCompanyId'] = value_set[0]
        values['TargetCompanyId'] = value_set[1]
        values['ExcludingDate'] = value_set[2]
        values['Note'] = value_set[3]
        values['CashPerShare'] = value_set[4]
        values['CashPerShareCurrency'] = value_set[5]

        return values

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = dict()
        param.update({'Package': 'EquityData',
                      'Content': 'MergerAndAcquisition',
                      'IdType': 'EquityCompanyId',
                      'Id': ''})
        param['Id'] = self.parse_line_value(line_value)['AcquirerCompanyId']

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
        dataId = int(value_set[1])
        return value_set[2]

    # 检查node
    def check_MergerAndAcquisition(self, target_node, target_values):
        if target_values['AcquirerCompanyId'] and \
                not target_values['AcquirerCompanyId'] \
                    == target_node.find('AcquirerCompanyId').text:
            return False
        if target_values['TargetCompanyId'] and \
                not target_values['TargetCompanyId'] \
                    == target_node.find('TargetCompanyId').text:
            return False
        if target_values['ExcludingDate'] and \
                not target_values['ExcludingDate'] \
                    == target_node.find('ExcludingDate').text:
            return False

        '''
        remove blank
        '''
        if target_values['Note'] and \
                not target_values['Note'].replace(" ", "") \
                    == target_node.find('Note').text.replace(" ", ""):
            return False
        if target_values['CashPerShare'] and \
                not float(target_values['CashPerShare']) \
                    == float(target_node.find('CashPerShare').text):
            return False
        if target_values['CashPerShareCurrency'] and \
                not target_values['CashPerShareCurrency'] \
                    == target_node.find('CashPerShareCurrency').text[-3:]:
            return False
        return True