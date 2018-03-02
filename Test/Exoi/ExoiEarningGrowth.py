# coding=utf-8
from ExoiType import ExoiType
import xml.etree.ElementTree as ET
from lxml import etree
import time


class ExoiEarningGrowth(ExoiType):

    def __init__(self):
        ExoiType.__init__(self)
        self.value_mapping = {
            13023: 'NormalizedBasicEPSGrowth'
        }

    # 检查传入的记录的值可以可以在xml中找到
    def check_value(self, line_value):
        flag = False
        values = self.parse_line_value(line_value)
        tree = ET.fromstring(self.content.encode('utf8'))  # unicode字符需要编码为utf8的字节型对象，这样才可以识别

        #使用xpath解析xml
        tree2 = etree.XML(self.content.encode('utf-8'))
        path = "/EarningGrowths[@shareClassId=\'"+values.get('shareClassId')+"\']/EarningGrowth[@reportType=\'" + values.get('reportType') + "\' and @fiscalYearEnd=\'"+values.get('fiscalYearEnd')+"\' and @asOf=\'"+values.get('asOf') + "\']/NormalizedBasicEPSGrowth/GrowthRate[@period=\'"+values.get('period')+"\']"
        target_node = tree2.xpath(path)
        if len(target_node) == 1 and target_node[0].text == values.get('NormalizedBasicEPSGrowth'):
            flag = True

        # 之前的用遍历的方式，太麻烦
        # if tree.attrib['shareClassId'] != values.get('shareClassId'):
        #     return flag
        #
        # for child in tree:  # 从xml中查到这些节点。
        #     asOf = child.attrib['asOf']
        #     fiscalYearEnd = child.attrib['fiscalYearEnd']
        #     reportType = child.attrib['reportType']
        #
        #     if asOf == values.get('asOf') and fiscalYearEnd == values.get('fiscalYearEnd') and reportType == values.get('reportType'):
        #         child.find()
        #
        #     check_count = 0  # 如果满足一个条件就加1，等于3的才是符合所有条件的
        #     companyId_str = child.find('CompanyId').text
        #     if companyId_str == values.get('CompanyId'):
        #         check_count += 1
        #
        #     AsOfDate_str = child.find('AsOfDate').text
        #     if AsOfDate_str == values.get('AsOfDate'):
        #         check_count += 1
        #
        #     DataId_name = self.value_mapping[int(line_value.split('|')[3])]
        #     DataId_str = child.find(DataId_name).text
        #     if DataId_str == values.get(DataId_name):
        #         check_count += 1
        #
        #     if check_count == 3:  # 如果找到了
        #         flag = True
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