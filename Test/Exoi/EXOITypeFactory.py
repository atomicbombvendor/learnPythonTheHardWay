# coding=utf-8
import time

from Test.Exoi.EXOIImpl.EXOITypeUKMajor import EXOITypeUKMajor
from Test.Exoi.EXOIImpl.EXOIEarningGrowths import EXOIEarningGrowths
from Test.Exoi.EXOIImpl.EXOIValuationRatios import EXOIValuationRatios
from Test.Exoi.EXOIImpl.EXOIOperationRatios import EXOIOperationRatios
from Test.Exoi.EXOIImpl.EXOIEarningReports import EXOIEarningReports
from Test.Exoi.EXOIImpl.EXOIEarningReportGTR import EXOIEarningReportGTR
from Test.Exoi.EXOIImpl.EXOIFinancialStatementGTR import EXOIFinancialStatementGTR
from Test.Exoi.EXOIImpl.EXOIFinancialStatements import EXOIFinancialStatements
from Test.Exoi.Logger import Logger
from Test.LogSingleton import LogSingleton


class EXOITypeFactory:

    def get_Exoi_Type(self, content):
        log_exoi = LogSingleton().get_logger()
        class_name = {
            # 返回类名
            'UKMajorShareholderTransactions': EXOITypeUKMajor,
            'EarningGrowths': EXOIEarningGrowths,
            'ValuationRatios': EXOIValuationRatios,
            'OperationRatios': EXOIOperationRatios,
            'EarningReports': EXOIEarningReports,
            'EarningReportGTR': EXOIEarningReportGTR,
            'FinancialStatementGTR': EXOIFinancialStatementGTR,
            'FinancialStatements': EXOIFinancialStatements
        }
        if class_name[content]:
            return class_name[content]()
        else:
            log_exoi.info("没有类名为"+content+" 请检查输入！")
