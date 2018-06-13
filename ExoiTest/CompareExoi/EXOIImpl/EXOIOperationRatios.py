# coding=utf-8
from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from lxml import etree
import time


class EXOIOperationRatios(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.value_mapping = {
            12044: 'NetIncomePerFullTimeEmployee',
            12045: 'SolvencyRatio',
            12046: 'ExpenseRatio',
            12047: 'LossRatio'
        }

        self.init_url = 'http://geexoidevap8002.morningstar.com/' \
                           'DataOutput.aspx?package=%s&Content=%s&IdType=%s' \
                           '&Id=%s&ReportType=%s&Dates=%s'

    # 检查传入的记录的值可以可以在xml中找到
    def check_value(self, line_value):
        flag = False
        values = self.parse_line_value(line_value)

        # 使用xpath解析xml
        tree2 = etree.XML(self.content.encode('utf-8'))
        path = "/OperationRatios[@companyId='"+values.get('companyId')\
               + "']/OperationRatio[@asOf='"+values.get('asOf')+"' and @reportType='"\
               + values.get('reportType')+"' and @fiscalYearEnd='"+values.get('fiscalYearEnd')\
               + "']/Profitability[@numberOfMonth='"+values.get('numberOfMonth')+"']/"\
               + values['targetNode']
        target_node = tree2.xpath(path)
        if len(target_node) == 1 and target_node[0].text == values.get('NetIncomePerFullTimeEmployee'):
            flag = True

        return flag

    # 把每一行的数据转换为一个字典，方便查询
    def parse_line_value(self, line_value):
        values = {
            'companyId': '',
            'asOf': '',
            'reportType': '',
            'fiscalYearEnd': '',
            'numberOfMonth': '',  # 如果是 3M,则是3;如果是1Y,则是12
            'NetIncomePerFullTimeEmployee': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['companyId'] = value_set[0]
        values['NetIncomePerFullTimeEmployee'] = value_set[2]
        values['targetNode'] = self.value_mapping.get(int(value_set[1]))
        values[self.value_mapping.get(int(value_set[1]))] = self.get_value(value_set)
        values['asOf'] = value_set[3]

        numberOfMonth = value_set[4]
        if numberOfMonth == '1Y':
            values['numberOfMonth'] = str(12)
        else:
            values['numberOfMonth'] = str(numberOfMonth[0:1])

        values['fiscalYearEnd'] = value_set[5]
        values['reportType'] = value_set[6]

        return values

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = {'Package': 'EquityData',
                 'Content': 'OperationRatio',
                 'IdType': 'EquityCompanyId',
                 'Id': '',
                 'Dates': '',
                 'ReportType': ''}

        values = line_value.split("|")
        Id = values[0]
        Dates = time.strptime(values[3], "%Y-%m-%d").tm_year
        param['NumberOfMonth'] = values[4]
        param['FiscalYearEnd'] = values[5]
        param['ReportType'] = values[6]
        param['Id'] = Id
        param['Dates'] = Dates

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

    def get_value(self, value_set):
        dataId = int(value_set[1])
        return value_set[2]