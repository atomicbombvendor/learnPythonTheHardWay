# coding=utf-8
import codecs

from ExoiTypeFactory import ExoiTypeFactory


class TestExoi:

    # 每次处理一个文件是，type和参数都是一样的（需要把Date的范围扩到最大）
    def __init__(self, file_type_):
        self.exoi_type = ExoiTypeFactory().get_Exoi_Type(file_type_)
        # self.exoi_type.get_content(file_param)
        self.not_match = []
        self.do_match = []

    # 判断每一行的数据是不是可以找到
    def test(self, line):
        file_param = self.exoi_type.parse_line(line)
        self.exoi_type.get_content(file_param)
        flag = self.exoi_type.check_value(line)
        if not flag:
            print u"节点不匹配 %s\n" %(line)
            self.not_match.append(line)
        else:
            print u"找到了节点了 %s\n" %(line)
            self.do_match.append(line)
        return flag

    def parse_line(self, line): pass

    # 读取文件，从文件中解析xml中的每一行
    def check_file(self, source_path, result_path):
        result = []
        file_object = codecs.open(source_path, 'r')
        try:
            for line in file_object:
                flag = self.test(line.strip("\n"))
                if not flag:
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
    file_type = 'EarningGrowth'
    line_value = '0P000005NU|13023|0.264399|2003-12-31|1Y|12|A'
    source_file ="D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\Delta\EarningRatiosAOR\\new_diff.dat"
    target_file ="D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\Delta\EarningRatiosAOR\\a.dat"
    test = TestExoi(file_type)
    # test.test(line_value)
    test.check_file(source_file, target_file)