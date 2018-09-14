# coding=utf-8
from ExoiTest.CompareExoi.EXOIImpl.EXOIPayRatio import EXOIPayRatio
from ExoiTest.CompareExoi.EXOIImpl.EXOISEDOL import EXOISEDOL
from ExoiTest.CompareExoi.EXOIImpl.EXOISecurityReference import EXOISecurityReference
from ExoiTest.CompareExoi.EXOIImpl.EXOIMergerAndAcquisition import EXOIMergerAndAcquisition
from ExoiTest.CompareExoi.EXOIImpl.EXOIEarningGrowths import EXOIEarningGrowths
from ExoiTest.CompareExoi.EXOIImpl.EXOIEarningReportGTR import EXOIEarningReportGTR
from ExoiTest.CompareExoi.EXOIImpl.EXOIEarningReports import EXOIEarningReports
from ExoiTest.CompareExoi.EXOIImpl.EXOIFinancialStatementGTR import EXOIFinancialStatementGTR
from ExoiTest.CompareExoi.EXOIImpl.EXOIFinancialStatements import EXOIFinancialStatements
from ExoiTest.CompareExoi.EXOIImpl.EXOIInsiderHolding import EXOIInsiderHolding
from ExoiTest.CompareExoi.EXOIImpl.EXOIOperationRatios import EXOIOperationRatios
from ExoiTest.CompareExoi.EXOIImpl.EXOITypeUKMajor import EXOITypeUKMajor
from ExoiTest.CompareExoi.EXOIImpl.EXOIValuationRatios import EXOIValuationRatios
from ExoiTest.CompareExoi.EXOIImpl.EXOIRealTime import EXOIRealTime
from ExoiTest.CompareExoi.EXOIImpl.EXOIAdvisors import EXOIAdvisor
from ExoiTest.CompareExoi.ExchangeRate.CurrencyExchangeRate import CurrencyExchangeRate
from ExoiTest.CompareExoi.Ownership.OwnershipDetail import OwnershipDetail
from ExoiTest.CompareExoi.Ownership.OwnershipMonthlySummary import OwnershipMonthlySummary
from ExoiTest.CompareExoi.Ownership.OwnershipSummary import OwnershipSummary
from ExoiTest.LogSingleton import LogSingleton


class EXOITypeFactory:

    def __init__(self):
        pass

    @staticmethod
    def get_Exoi_Type(content):
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
            'FinancialStatements': EXOIFinancialStatements,
            'RealTime': EXOIRealTime,
            'InsiderHolding': EXOIInsiderHolding,
            'ExchangeRate': CurrencyExchangeRate,
            'MergerAndAcquisition': EXOIMergerAndAcquisition,
            'Advisor': EXOIAdvisor,
            'SecurityReference': EXOISecurityReference,
            'PayRatio': EXOIPayRatio,
            'SEDOL': EXOISEDOL,
            'OwnershipSummary': OwnershipSummary,
            'OwnershipMonthlySummary': OwnershipMonthlySummary,
            'OwnershipDetail': OwnershipDetail
        }
        if class_name[content]:
            return class_name[content]()
        else:
            log_exoi.info("没有类名为" + content + " 请检查输入！")
