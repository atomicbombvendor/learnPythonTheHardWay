# coding=utf-8
import pickle

import os
from lxml import etree
from Test.PareEXOIXml.AbstractEXOI import AbstractEXOI


class EXOIParseFinancialStatement(AbstractEXOI):

    '''
    主要把EXOI返回的XML转换为对应的GEDF文件的格式。每一个点一行记录。
    GEDF FinancialStatement的格式是：
    0C000008A4|26005|-1213300000.000000|2017-09-30|9M|12|USD|A|0
    {CompanyId}|{DataId}|{DataValue}|{asOf}|{numberOfMonth}|{fiscalYearEnd}|{reportType}|{isDerived}
    URL的参数需要有 CompanyId，ReportType，Year.
    '''
    def __init__(self):
        AbstractEXOI.__init__(self)
        self.init_url = 'http://geexoidevap8002.morningstar.com/' \
                           'DataOutput.aspx?package=%s&Content=%s&IdType=%s' \
                           '&Id=%s&ReportType=%s&Dates=%s'

    def start_parse(self, file_path=""):
        tree2 = etree.XML(self.content.encode('utf-8'))
        dump_file_name = os.path.join(file_path,
                                      "FinancialStatement_%s_%s.dat" % (self.full_url_param['Id'], self.full_url_param['ReportType']))
        with open(dump_file_name, "w") as t:
            pickle.dump(self.content, t)
            print("持久化数据文件成功")

    #  产生完整的URL
    def construct_full_url(self, param):
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

    # 根据通用的参数,加入FinancialStatement需要的其他URL参数
    def construct_full_param(self, parm):
        self.full_url_param = {
            'Package': 'EquityData',
            'Content': 'Fundamental',
            'IdType': 'EquityCompanyId',
            'Id': parm["Id"],
            'Dates': parm['Year'],
            'ReportType': parm['ReportType']}