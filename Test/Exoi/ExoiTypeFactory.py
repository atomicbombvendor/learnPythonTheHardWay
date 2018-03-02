# coding=utf-8
from ExoiTypeUKMajor import ExoiTypeUKMajor
from ExoiEarningGrowth import ExoiEarningGrowth


class ExoiTypeFactory:

    def get_Exoi_Type(self, content):
        map_ = {
            # 这里初始化map的时候，会初始化对象两次。所以会登录
            'UKMajorShareholderTransactions': ExoiTypeUKMajor(),
            'EarningGrowth': ExoiEarningGrowth()
        }
        return map_[content]
