from ExoiTypeUKMajor import ExoiTypeUKMajor


class ExoiTypeFactory:

    def get_Exoi_Type(self, content):
        map_ = {
            'UKMajorShareholderTransactions': ExoiTypeUKMajor()
        }
        return map_[content]
