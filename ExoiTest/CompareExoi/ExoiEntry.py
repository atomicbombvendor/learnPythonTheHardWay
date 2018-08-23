# coding=utf-8
import ConfigParser
import codecs
from datetime import datetime
from multiprocessing import cpu_count, Pool

from ExoiTest import myglobal
from ExoiTest.CompareExoi.EXOITypeFactory import EXOITypeFactory


class TestExoi:

    # 每次处理一个文件是，type和参数都是一样的（需要把Date的范围扩到最大）
    def __init__(self, file_type_):
        self.log_exoi = myglobal.get_logger()
        self.exoi_type = EXOITypeFactory().get_Exoi_Type(file_type_)
        self.not_match = []
        self.do_match = []

    # 判断每一行的数据是不是可以找到
    # 先把文件中的每一行转换为一个参数字典，在把字典和url对应起来。
    def start_check_line(self, line):
        starttime = datetime.now()
        file_param = self.exoi_type.parse_line(line)
        endtime = datetime.now()
        # self.log_exoi.info("Parse Line take %dms" % ((endtime-starttime).microseconds/1000))

        starttime = datetime.now()
        self.exoi_type.get_content(file_param)
        endtime = datetime.now()
        # self.log_exoi.info("Read Content take %dms" % ((endtime - starttime).microseconds / 1000))

        starttime = datetime.now()
        flag = self.exoi_type.check_value(line)
        endtime = datetime.now()
        # self.log_exoi.info("Check Value take %dms" % ((endtime - starttime).microseconds / 1000))

        if not flag:
            self.log_exoi.info(u"节点不匹配 %s\n" % line)
            self.not_match.append(line)
        else:
            self.log_exoi.info(u"找到了节点了 %s\n" % line)
            self.do_match.append(line)
        return flag

    def parse_line(self, line): pass

    # 读取文件，从文件中解析xml中的每一行
    def check_file(self, source_path, result_path):
        self.log_exoi.info("Start check file: {0}".format(source_path))
        all_node_exists = True
        result = []
        file_object = codecs.open(source_path, 'r')
        try:
            for line in file_object:
                flag = self.start_check_line(line.strip("\n"))
                if not flag:
                    all_node_exists = False
                    result.append(line)
            self.write_file(result_path, result)

            if not all_node_exists:
                self.log_exoi.info(u"不是所有的节点都可以找到")  # 报错是因为这里是中文字符，需要转换为unicode字符
            else:
                self.log_exoi.info(u"所有的节点都可以找到")  # u表示是unicode字符。

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
        'FinancialStatements',
        'RealTime',
        'InsiderHolding',
        'ExchangeRate',
        'MergerAndAcquisition',
        'Advisor',
        'SecurityReference'
    }

    file_type = None
    for type_r in file_types:
        if type_r in section_inputs:
            file_type = type_r
    if file_type:
        return file_type
    else:
        print("Can't mapping special file" + section_inputs + " to class type")


# 读取配置文件中的和某个关键字有关的Section, 然后比较所有的文件
# 这是单线程的版本, 多进程的版本,在multi_process
def batch_test(section_input):
    conf = ConfigParser.ConfigParser()
    conf.read('../ConfigFile/CompareExoi_File_Config.ini')
    file_sections = conf.sections()
    for section in file_sections:
        if section_input in section:
            single_test(section)


# 读取配置文件中和section_name匹配的Section, 然后比较文件
# 只能比较一个具体的文件
def single_test(section_input):
    # 主进程与子进程是并发执行的，进程之间默认是不能共享全局变量的
    fileType = get_file_types(section_input)
    test = TestExoi(fileType)
    conf = ConfigParser.ConfigParser()
    conf.read('../ConfigFile/CompareExoi_File_Config.ini')
    source_file = conf.get(section_input, 'source_file')
    target_file = conf.get(section_input, 'target_file')
    myglobal.get_logger().info("Verify File ***********" + section_input)
    test.check_file(source_file, target_file)


# 多进程的运行. 是batch_test的多进程版本.
# 因为是多个参数,没有使用Map
def multi_process(target_section):
    conf = ConfigParser.ConfigParser()
    conf.read('../ConfigFile/CompareExoi_File_Config.ini')
    file_sections = conf.sections()
    pool = Pool(processes=cpu_count())  # 根据CPU的核心创建进程数
    for section_input in file_sections:
        if target_section in section_input:
            pool.apply_async(single_test, args=(section_input,))
    pool.close()
    pool.join()
    myglobal.get_logger().info(str("All file process done"))


# 修改logger配置文件的内容
def modify_log_file_name(file_name):
    content = ""
    log_file = "../resource/logconfig.conf"
    with codecs.open(log_file, "r", "utf-8") as f:
        for line in f:
            if "log_file" in line:
                content += "log_file = d:/QA/Log/EXOI_%s_CheckWithEXOI_@time@.log\r\n" % (file_name)
            else:
                content += line

    with codecs.open(log_file, "wb", "utf-8") as f:
        f.write(content)


# 比较source_file中的每一行记录,把不匹配的记录记录在target_file文件中.
# 要做的几件检查:
# 1. 如果是新的文件类型,需要保证节点名要出现在get_file_types方法中的列表;
# 2. 如果是新的文件类型,需要保证EXOITypeFactory的工厂中有该文件类型;
# 3. 如果是新添加的点,需要保证对应的Impl类中有新添加的点;
if __name__ == '__main__':
    target_section_para = 'MOCAL5284_Delta_NRA_Fundamental_FinancialStatements'
    modify_log_file_name(target_section_para)  # 指定Logger文件存放的位置
    batch_test("MOCAL5284_Delta_NRA_Fundamental_FinancialStatements")
    # multi_process(target_section_para)
    # single_test("MOCAL5284_Delta_NRA_Fundamental_FinancialStatements")
    # single_test("R20180531_Monthly_NRA_InsiderHolding")
    # single_test(target_section_para)
