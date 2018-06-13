# coding=utf-8
from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from lxml import etree
import time


class EXOIEarningGrowths(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.value_mapping = {
            13023: 'NormalizedBasicEPSGrowth'
        }

        self.init_url = 'http://geexoidevap8002.morningstar.com/' \
                        'DataOutput.aspx?package=%s&Content=%s&IdType=%s' \
                        '&Id=%s&ReportType=%s&Dates=%s'

    # 检查传入的记录的值可以可以在xml中找到
    def check_value(self, line_value):
        flag = False
        values = self.parse_line_value(line_value)
        # 使用xpath解析xml
        tree2 = etree.XML(self.content.encode('utf-8'))  # unicode字符需要编码为utf8的字节型对象，这样才可以识别
        path = "/EarningGrowths[@shareClassId=\'"+values.get('shareClassId')+"\']/EarningGrowth[@reportType=\'" + values.get('reportType') + "\' and @fiscalYearEnd=\'"+values.get('fiscalYearEnd')+"\' and @asOf=\'"+values.get('asOf') + "\']/NormalizedBasicEPSGrowth/GrowthRate[@period=\'"+values.get('period')+"\']"
        target_node = tree2.xpath(path)
        if len(target_node) == 1 and target_node[0].text == values.get('NormalizedBasicEPSGrowth'):
            flag = True

        return flag

    def parse_line_value(self, line_value):
        values = {
            'shareClassId': '',
            'reportType': '',
            'asOf': '',
            'fiscalYearEnd': '',
            'period': '',
            'NormalizedBasicEPSGrowth': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['shareClassId'] = value_set[0]
        values['NormalizedBasicEPSGrowth'] = value_set[2]
        values['asOf'] = value_set[3]
        values['period'] = value_set[4]
        values['fiscalYearEnd'] = value_set[5]
        values['reportType'] = value_set[6]

        return values

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = {'Package': 'EquityData',
                 'Content': 'EarningGrowth',
                 'IdType': 'EquityShareClassId',
                 'Id': '',
                 'Dates': '',
                 'ReportType': ''}

        values = line_value.split("|")
        Id = values[0]
        Dates = time.strptime(values[3], "%Y-%m-%d").tm_year
        ReportType = values[6]
        param['Id'] = Id
        param['Dates'] = Dates
        param['ReportType'] = ReportType

        return param

    # 产生完整的URL
    def construct_url(self, param):
        # 把所有的key转换为小写的
        a_lower = {k.lower(): v for k, v in param.items()}
        package = a_lower.get('package'.lower())
        content = a_lower.get('content'.lower())
        Id = a_lower.get('Id'.lower())
        IdType = a_lower.get('IdType'.lower())
        Dates = a_lower.get('Dates'.lower())
        ReportType = a_lower.get('ReportType'.lower())
        intact_url = self.init_url % (package, content, IdType, Id, ReportType, Dates)
        return intact_url