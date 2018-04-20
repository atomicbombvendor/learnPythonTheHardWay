# coding=utf-8
from Test.Exoi.AbstractEXOI import AbstractEXOI
from lxml import etree
import time


class EXOIEarningReports(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.value_mapping = {
            20001: '@periodEndingDate',
            20002: '@fileDate',
            20003: '@accessionNumber',
            20004: '@formType',
            29000: 'BasicContinuousOperations',
            29001: 'BasicDiscontinuousOperations',
            29002: 'BasicExtraordinary',
            29003: 'BasicAccountingChange',
            29004: 'BasicEPS',
            29005: 'DilutedContinuousOperations',
            29006: 'DilutedDiscontinuousOperations',
            29007: 'DilutedExtraordinary',
            29008: 'DilutedAccountingChange',
            29009: 'DilutedEPS',
            29010: 'BasicAverageShares',
            29011: 'DilutedAverageShares',
            29012: 'DividendPerShare',
            29013: 'BasicEPSOtherGainsLosses',
            29014: 'ContinuingAndDiscontinuedBasicEPS',
            29015: 'TaxLossCarryforwardBasicEPS                     ',
            29016: 'DilutedEPSOtherGainsLosses',
            29017: 'ContinuingAndDiscontinuedDilutedEPS',
            29018: 'TaxLossCarryforwardDilutedEPS',
            29019: 'NormalizedBasicEPS',
            29020: 'NormalizedDilutedEPS',
            29021: 'TotalDividendPerShare',
            28005: '@isFYC',
            29022: 'ReportedNormalizedBasicEPS',
            29023: 'ReportedNormalizedDilutedEPS',
            29024: 'DividendCoverageRatio'
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

        # 如果DataId节点不存在
        if values['targetNode'] is None:
            self.log_exoi.error("没有找到与%s对应的节点名" % line_value.split('|')[1])
            return

        if "@" not in values['targetNode']:
            path = "/EarningReports[@shareClassId='"+values.get('shareClassId')\
               + "']/EarningReport[@asOf='"+values.get('asOf')+"' and @reportType='"\
               + values.get('reportType')+"' and @fiscalYearEnd='"+values.get('fiscalYearEnd')\
               + "' and @numberOfMonth='"+values.get('numberOfMonth') + "' and @currencyId='" + values.get('currencyId') \
               + "' and @isDerived='"+values.get('isDerived')+"']/"\
               + values['targetNode']
            target_node = tree2.xpath(path)
            if len(target_node) == 1 and target_node[0].text == values.get(values.get('targetNode')):
                flag = True
        else:
            path = "/EarningReports[@shareClassId='" + values.get('shareClassId') \
                   + "']/EarningReport[@asOf='" + values.get('asOf') + "' and @reportType='" \
                   + values.get('reportType') + "' and @fiscalYearEnd='" + values.get('fiscalYearEnd') \
                   + "' and @numberOfMonth='" + values.get('numberOfMonth') + "' and @currencyId='" + values.get(
                'currencyId') \
                   + "' and @isDerived='" + values.get('isDerived') + "' and "+values.get('targetNode')+"='" + values.get(values.get('targetNode')) + "']"  # only need get attr
            target_node = tree2.xpath(path)
            if len(target_node) == 1:
                flag = True

        return flag

    # 把每一行的数据转换为一个字典，方便查询
    def parse_line_value(self, line_value):
        values = {
            'shareClassId': '',
            'asOf': '',
            'reportType': '',
            'fiscalYearEnd': '',
            'numberOfMonth': '',
            'isDerived': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['shareClassId'] = value_set[0]
        values['targetNode'] = self.value_mapping.get(int(value_set[1]))
        values[self.value_mapping.get(int(value_set[1]))] = value_set[2]
        values['asOf'] = value_set[3]
        values['numberOfMonth'] = value_set[4].replace('M', "")
        values['fiscalYearEnd'] = value_set[5]
        values['currencyId'] = 'CU$$$$$' + value_set[6]
        values['reportType'] = value_set[7]
        values['isDerived'] = value_set[8]

        return values

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = {'Package': 'EquityData',
                 'Content': 'EarningReport',
                 'IdType': 'EquityShareClassId',
                 'Id': '',
                 'Dates': '',
                 'ReportType': ''}

        values = line_value.split("|")
        Id = values[0]
        Dates = time.strptime(values[3], "%Y-%m-%d").tm_year
        reportType = values[7]
        param['ReportType'] = reportType
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