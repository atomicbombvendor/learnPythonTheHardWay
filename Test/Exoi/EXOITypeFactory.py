# coding=utf-8
from EXOITypeUKMajor import EXOITypeUKMajor
from EXOIEarningGrowth import EXOIEarningGrowth
from EXOIValuationRatios import EXOIValuationRatios
from EXOIOperationRatios import EXOIOperationRatios
from EXOIEarningReport import EXOIEarningReport


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
            'EXOIEarningReport': EXOIEarningReport
        }
        if class_name[content]:
            return class_name[content]()
        else:
            print "没有类名为", content, " 请检查输入！"
