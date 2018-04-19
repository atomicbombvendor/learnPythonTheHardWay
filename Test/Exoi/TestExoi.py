# coding=utf-8
import codecs
import ConfigParser
from multiprocessing import cpu_count, Pool
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
            print u"节点不匹配 %s\n" % line
            self.not_match.append(line)
        else:
            print u"找到了节点了 %s\n" % line
            self.do_match.append(line)
        return flag

    def parse_line(self, line): pass

    # 读取文件，从文件中解析xml中的每一行
    def check_file(self, source_path, result_path):
        print("Start check file: {0}".format(source_path))
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


# 根据section中的是不是包含了fileType,返回具体的fileType
def get_file_types(section_inputs):
    file_types = {
        # 返回类名
        'UKMajorShareholderTransactions',
        'EarningGrowths',
        'ValuationRatios',
        'OperationRatios',
        'EarningReports',
        'EarningReportGTR',
        'FinancialStatementGTR',
        'FinancialStatements'
    }

    for type_r in file_types:
        if type_r in section_inputs:
            return type_r


# 读取配置文件中的和某个关键字有关的Section, 然后比较所有的文件
# 这是单线程的版本, 多进程的版本,在multi_process
def batch_test(section_input):
    fileType = get_file_types(section_input)
    test = TestExoi(fileType)
    conf = ConfigParser.ConfigParser()
    conf.read('MOCAL_File_Config.ini')
    file_sections = conf.sections()
    for section in file_sections:
        if section_input in section:
            source_file = conf.get(section, 'source_file')
            target_file = conf.get(section, 'target_file')
            print "Verify File ***********" + section
            test.check_file(source_file, target_file)


# 读取配置文件中和section_name匹配的Section, 然后比较文件
# 只能比较一个具体的文件
def single_test(section_input):
    fileType = get_file_types(section_input)
    test = TestExoi(fileType)
    conf = ConfigParser.ConfigParser()
    conf.read('MOCAL_File_Config.ini')
    source_file = conf.get(section_input, 'source_file')
    target_file = conf.get(section_input, 'target_file')
    print "Verify File ***********" + section_input
    test.check_file(source_file, target_file)


# 多进程的运行. 是batch_test的多进程版本.
# 因为是多个参数,没有使用Map
def multi_process(target_section):
    conf = ConfigParser.ConfigParser()
    conf.read('MOCAL_File_Config.ini')
    file_sections = conf.sections()
    pool = Pool(processes=cpu_count())  # 根据CPU的核心创建进程数
    for section_input in file_sections:
        if target_section in section_input:
            pool.apply_async(single_test, args=(section_input,))
    pool.close()
    pool.join()


# 比较source_file中的每一行记录,把不匹配的记录记录在target_file文件中.
if __name__ == '__main__':
    target_section_para = 'MOCAL4169'
    multi_process(target_section_para)
