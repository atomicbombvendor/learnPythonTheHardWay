# coding=utf-8

from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from lxml import etree


class EXOIPayRatio(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.value_mapping = {
            44006: 'SharesPercentage',
            44008: 'SharesPercentage',
            60101: 'ReportDate',
            60102: 'ReportSource',
            60117: 'Currency',
            82001: 'CEOPay',
            82002: 'MedianEmployeePay',
            82003: 'PayRatioCompensationMethod',
            82004: 'PayRatioEmployeeCountMethod',
            82005: 'AdditionalDescription',
            82006: 'PayRatio'
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
        path = "/CompanyPayRatio[@CompanyId='{companyId}']/FiscalYear[@Year='{fiscalYear}']/"\
               "PayRatioInformation[@PersonId='{personId}' and {targetNode}='{targetNode_value}']"\
                   .format(companyId=values.get('companyId'), fiscalYear=values.get('fiscalYear'),
                           personId=values.get('personId'),
                           targetNode=values['targetNode'], targetNode_value=values.get(values.get('targetNode')))
        target_node = tree2.xpath(path)
        if len(target_node) >= 1 and target_node[0].find('ReportDate').text[0:4] == values['reportYear']:
            flag = True

        return flag

    # 把每一行的数据转换为一个字典，方便查询
    def parse_line_value(self, line_value):
        values = {
            'companyId': ''}
        value_set = line_value.split('|')  # value_set最后的两个要被解析成节点和值的对应
        values['companyId'] = value_set[0]
        values['reportYear'] = value_set[1]
        values['fiscalYear'] = value_set[2]
        values['personId'] = value_set[3]
        values['targetNode'] = self.value_mapping.get(int(value_set[4]))
        values[self.value_mapping.get(int(value_set[4]))] = self.get_value(value_set)

        return values

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = {'Package': 'EquityData',
                 'Content': 'PayRatio',
                 'IdType': 'EquityCompanyId',
                 'Id': ''}

        values = line_value.split("|")
        Id = values[0]
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
        return value_set[5]
