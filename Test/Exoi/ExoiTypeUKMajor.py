# coding=utf-8
from ExoiType import ExoiType
import xml.etree.ElementTree as ET


class ExoiTypeUKMajor(ExoiType):

    def __init__(self):
        ExoiType.__init__(self)
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

    # 检查传入的记录的值可以可以在xml中找到
    def check_value(self, line_value):
        flag = False
        values = self.parse_line_value(line_value)
        tree = ET.fromstring(self.content.encode('utf8'))  # unicode字符需要编码为utf8的字节型对象，这样才可以识别

        if tree.attrib['ShareClassId'] != values.get('ShareClassId'):
            return flag

        for child in tree:  # 从xml中查到这些节点。
            check_count = 0  # 如果满足一个条件就加1，等于3的才是符合所有条件的
            companyId_str = child.find('CompanyId').text
            if companyId_str == values.get('CompanyId'):
                check_count += 1

            AsOfDate_str = child.find('AsOfDate').text
            if AsOfDate_str == values.get('AsOfDate'):
                check_count += 1

            DataId_name = self.value_mapping[int(line_value.split('|')[3])]
            DataId_str = child.find(DataId_name).text
            if DataId_str == values.get(DataId_name):
                check_count += 1

            if check_count == 3:  # 如果找到了
                flag = True
        return flag

    # 解析每一行的数据，把属性和值对应起来
    def parse_line_value(self, line_value):
        values = {
            'ShareClassId': '',
            'CompanyId': '',
            'AsOfDate': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['ShareClassId'] = value_set[0]
        values['AsOfDate'] = value_set[1]
        values['CompanyId'] = value_set[2]
        values[self.value_mapping[int(value_set[3])]] = value_set[4]
        return values
