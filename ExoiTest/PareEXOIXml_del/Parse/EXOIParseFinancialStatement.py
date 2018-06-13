# coding=utf-8
import pickle

import os
from lxml import etree

from ExoiTest.PareEXOIXml_del.AbstractEXOI import AbstractEXOI


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
                                      "FinancialStatement_%s_%s.dat" % (
                                      self.full_url_param['Id'], self.full_url_param['ReportType']))
        with open(dump_file_name, "w") as t:
            pickle.dump(self.content, t)
            print("持久化数据文件成功")

        # region 简单遍历的方案不可取
        print(tree2.tag, ":", tree2.attrib)  # 打印根元素的tag和属性
        id = tree2.attrib['companyId']
        # 遍历xml文档的第二层
        for child in tree2:
            # 第二层节点的标签名称和属性
            print(child.tag, ":", child.attrib)
            # 遍历xml文档的第三层
            for children in child:
                # 第三层节点的标签名称和属性
                fiscalYearEnd = children.attrib['fiscalYearEnd']
                currencyId = children.attrib['currencyId'][7:10]
                numberOfMonth = children.attrib['numberOfMonth'] + "M"
                reportType = children.attrib['reportType']
                asOf = children.attrib['asOf']
                if not children.attrib['isDerived']:
                    isDerived = "0"
                else:
                    isDerived = children.attrib['isDerived']

                print(children.tag, ":", children.attrib)
                # BalanceSheets没有isDerived.
                for grandchild in children:
                    tag = grandchild.tag
                    value = grandchild.text
                    print(grandchild.tag, ":", grandchild.text)
        # endregion

        # 应当采取GEDF代码中的方式来做
        # IncomeStatementDpList = DataPointXOIMappingSrv.GetDataPoints("FinanicalIncomeStatementsDataPoint");
        # BalanceSheetsDpList = DataPointXOIMappingSrv.GetDataPoints("FinanicalBalanceSheetsDataPoint");
        # CashFlowsDpList = DataPointXOIMappingSrv.GetDataPoints("FinanicalCashFlowsDataPoint");
        # MiscFinancialDataDpList = DataPointXOIMappingSrv.GetDataPoints("FinanicalMiscFinancialDataDataPoint");
        #
        # IncomeStatementsNodeList = doc.SelectNodes("/FinancialReports/IncomeStatements/IncomeStatement");
        # BalanceSheetsDateNodeList = doc.SelectNodes("/FinancialReports/BalanceSheets/BalanceSheet");
        # CashFlowsDateNodeList = doc.SelectNodes("/FinancialReports/CashFlows/CashFlow");
        # MiscFinancialDataNodeList = doc.SelectNodes("/FinancialReports/MiscFinancialData/MiscInfo");


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
