# coding=utf-8
import codecs

from ExoiTypeFactory import ExoiTypeFactory


class TestExoi:

    # 每次处理一个文件是，type和参数都是一样的（需要把Date的范围扩到最大）
    def __init__(self, file_type_, file_param):
        self.exoi_type = ExoiTypeFactory().get_Exoi_Type(file_type_)
        self.exoi_type.get_content(file_param)

    def test(self, line):
        flag = self.exoi_type.check_value(line)
        if not flag:
            print u"不匹配"
        else:
            print u"找到了"

    # 读取文件，从文件中解析xml中的每一行
    def check_file(self, source_path, result_path):
        result = []
        file_object = codecs.open(source_path, 'r')
        try:
            for line in file_object:
                if not self.exoi_type.check_value(line):
                    result.append(line)
            self.write_file(result_path, result)
        finally:
            file_object.close()

    # 把结果写入到文件中
    @staticmethod
    def write_file(result_path, data):
        file_object = codecs.open(result_path, 'w', 'utf-8')  # w会清空原来的内容 a为追加
        for i in data:
            file_object.write(str(i) + '\r\n')  # \r\n为换行符
        file_object.close()


if __name__ == '__main__':
    file_type = 'UKMajorShareholderTransactions'
    param = {'Package': 'EquityData',
             'Content': 'UKMajorShareholderTransactions',
             'IdType': 'EquityShareClassId',
             'Id': '0P00007NZP',
             'Dates': '2017,2016,2015,2014,2013,2012,2011,2010,2009,2008',
             'ReportType': 'A'}
    line_value = '0P00007NZP|2015-05-07|0C000006UD|46002|B'
    test = TestExoi(file_type, param)
    test.test(line_value)