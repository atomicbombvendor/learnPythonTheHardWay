# coding=utf-8
import codecs
import ConfigParser
from Test.Exoi.EXOITypeFactory import EXOITypeFactory


class TestExoi:

    # 每次处理一个文件是，type和参数都是一样的（需要把Date的范围扩到最大）
    def __init__(self, file_type_):
        self.exoi_type = EXOITypeFactory().get_Exoi_Type(file_type_)
        # self.exoi_type.get_content(file_param)
        self.not_match = []
        self.do_match = []

    # 判断每一行的数据是不是可以找到
    # 先把文件中的每一行转换为一个参数字典，在把字典和url对应起来。
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
        all_node_exists = True
        result = []
        file_object = codecs.open(source_path, 'r')
        try:
            for line in file_object:
                flag = self.test(line.strip("\n"))
                if not flag:
                    all_node_exists = False
                    result.append(line)
            self.write_file(result_path, result)

            if not all_node_exists:
                print "不是所有的节点都可以找到"

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
    file_type = 'EXOIEarningReportGTR'
    MOCALFile_Section = '4973_EarningReport_UKI_Restate'
    conf = ConfigParser.ConfigParser()
    conf.read('MOCAL_File_Config.ini')
    source_file = conf.get(MOCALFile_Section, 'source_file')
    target_file = conf.get(MOCALFile_Section, 'target_file')
    print "Verify File ***********" + MOCALFile_Section
    test = TestExoi(file_type)
    # test.test(line_value)
    test.check_file(source_file, target_file)
