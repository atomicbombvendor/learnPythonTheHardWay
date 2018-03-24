# coding=utf-8
from Test.Exoi.EXOIImpl.EXOITypeUKMajor import EXOITypeUKMajor
from Test.Exoi.EXOIImpl.EXOIEarningGrowth import EXOIEarningGrowth
from Test.Exoi.EXOIImpl.EXOIValuationRatios import EXOIValuationRatios
from Test.Exoi.EXOIImpl.EXOIOperationRatios import EXOIOperationRatios
from Test.Exoi.EXOIImpl.EXOIEarningReport import EXOIEarningReport
from Test.Exoi.EXOIImpl.EXOIEarningReportGTR import EXOIEarningReportGTR
from Test.Exoi.EXOIImpl.EXOIFinancialStatementGTR import EXOIFinancialStatementGTR



class EXOITypeFactory:

    def get_Exoi_Type(self, content):
        # map_ = {
        #     # 这里初始化map的时候，会初始化对象两次。所以会登录
        #     'UKMajorShareholderTransactions': EXOITypeUKMajor(),
        #     'EarningGrowth': EXOIEarningGrowth(),
        #     'ValuationRatios': EXOIValuationRatios(),
        #     'OperationRatios': EXOIOperationRatios(),
        #     'EXOIEarningReport': EXOIEarningReport()
        # }

        class_name = {
            # 返回类名
            'UKMajorShareholderTransactions': EXOITypeUKMajor,
            'EarningGrowth': EXOIEarningGrowth,
            'ValuationRatios': EXOIValuationRatios,
            'OperationRatios': EXOIOperationRatios,
            'EXOIEarningReport': EXOIEarningReport,
            'EXOIEarningReportGTR': EXOIEarningReportGTR,
            'EXOIFinancialStatementGTR': EXOIFinancialStatementGTR,
        }
        if class_name[content]:
            return class_name[content]()
        else:
            print "没有类名为", content, " 请检查输入！"
