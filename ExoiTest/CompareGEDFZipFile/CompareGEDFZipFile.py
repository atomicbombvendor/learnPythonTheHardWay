# coding=utf-8
import codecs
import datetime
import gzip
import logging
import re
import zipfile
import ConfigParser
import os


def getLogger(section_name):
    log_filename = "D:/QA/Log/EXOI_%s_CompareGEDFZip_%s.log" % (section_name, datetime.datetime.now().strftime('%Y-%m-%d'))
    logger = logging.getLogger(__name__)
    # filter = logging.Filter(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    file_handler = logging.FileHandler(log_filename, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    # file_handler.addFilter(filter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    # file_handler.addFilter(filter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


class CompareGEDFZipFile:

    def __init__(self, log_sectionName):

        self.logger = getLogger(log_sectionName)
        self.conf = ConfigParser.ConfigParser()
        self.conf.read('../ConfigFile/CompareZip_File_Config.ini')

    def init_param(self, section_name):
        self.section_name = section_name
        self.source_master = self.conf.get(section_name, 'source_master')
        self.source_new_branch = self.conf.get(section_name, 'source_new_branch')
        self.result = self.conf.get(section_name, 'result') + "\\" + section_name
        try:
            dataId_index_t = self.conf.get(section_name, 'dataId_index')  # 用来确定DataId所在的位置, 默认为1
            self.dataId_index = int(dataId_index_t)
        except ConfigParser.NoOptionError, e:
            self.dataId_index = 1

    # 读取压缩文件，返回压缩文件内的文件 gz
    def read_gz_file(self, file):
        if os.path.exists(file):
            with gzip.open(file, 'r') as pf:
                for line in pf:
                    yield line
        else:
            self.logger.error('the path [{}] is not exist!'.format(file))

    '''
    读取压缩包文件，返回读取的内容
    '''
    def readZipContent(self, file):

        if not os.path.exists(file):
            logging.info("the file %s is not exists ".format())
            return None

        zfile = zipfile.ZipFile(file, 'r')
        data = ''
        count = 0.0
        file_counts = len(zfile.namelist())
        percenet = 0
        for filename in zfile.namelist():
            count += 1.0
            data += zfile.read(filename)
            current_percenet = (count / file_counts) * 100
            if current_percenet - percenet >= 10:
                percenet = current_percenet
                # print("have processed %d%%" % percenet)
        return data

    @staticmethod
    def read_id_from_zip(file):
        zfile = zipfile.ZipFile(file, 'r')
        pattern = r"(0P[0-9A-Za-z]{8}|0C[0-9A-Za-z]{8})"
        data = ''
        for filename in zfile.namelist():
            match = re.search(pattern, filename)
            if match:
                data += match.group() + "\r\n"
        return data

    # 把data放入set中
    def get_set(self, data):
        result = set()
        if not data:
            return result
        # if getattr(data, '__iter__', None):
        lines = data.split('\r\n')
        for line in lines:
            result.add(line)
        return result

    # 比较文件不同，返回比较结果
    def compareFiles(self, old, new):
        sd = set(old)
        sl = set(new)
        return sd - sl, sl - sd

    # 将不同写入文件
    # old, new比较的结果
    # path 存放结果的文件夹路径
    # 存放结果的文件名 old_result_file, new_result_file
    def write_file(self, old, new, path, old_result_file, new_result_file):
        if len(list(old)) > 0:
            self.logger.info("Old is not null ")
            self.logger.info("DataIds in old>> " + " ".join(self.get_all_dataId(old)))
        else:
            self.logger.info("Old is null ")
        if len(list(new)) > 0:
            self.logger.info("new is not null ")
            self.logger.info("DataIds in new>> " + " ".join(self.get_all_dataId(new)))
        else:
            self.logger.info("new is null ")

        if not os.path.exists(path):
            os.makedirs(path)  # 创建级联目录
        with codecs.open(old_result_file, 'w', 'utf-8') as fnl:
            for line in list(old):
                fnl.write((str(line) + "\r\n").decode(encoding='utf-8'))
        with codecs.open(new_result_file, 'w', 'utf-8') as fnd:
            for line in list(new):
                fnd.write((str(line) + "\r\n").decode(encoding='utf-8'))

    # 开始测试流程，主方法入口
    def test(self):
        self.logger.info("Start Compare File >>> " + self.section_name)
        result_old = self.result + '\old_diff.dat'
        result_new = self.result + '\\new_diff.dat'
        self.logger.info("Read Zip File Content")
        file_data_old = self.readZipContent(self.source_master)
        file_data_new = self.readZipContent(self.source_new_branch)

        self.logger.info("Parse Zip File Content")
        set_old = self.get_set(file_data_old)
        set_new = self.get_set(file_data_new)

        # set_old是标准文件，set_new是新产生的文件
        # diff_old是只在old中存在的； diff_new 是只在新文件中存在的
        self.logger.info("Compare Zip File Content")
        diff_old, diff_new = self.compareFiles(set_old, set_new)
        if not diff_old and not diff_new:
            self.logger.info("All zip files have same content.")
        self.write_file(diff_old, diff_new, self.result, result_old, result_new)
        self.logger.info("Compare File Done\r\n")

    # 读取配置文件中的和某个关键字有关的Section, 然后比较所有的文件
    @staticmethod
    def batch_test(section_num_name):
        conf = ConfigParser.ConfigParser()
        conf.read('../ConfigFile/CompareZip_File_Config.ini')
        file_sections = conf.sections()
        test = CompareGEDFZipFile(section_num_name)
        for section in file_sections:
            if section_num_name in section:
                # self.logger.info("Start Compare File >>> " + section)
                test.init_param(section)
                test.test()

    # 读取配置文件中和section_name匹配的Section, 然后比较文件
    @staticmethod
    def single_test(section_name):
        file_section = section_name
        # self.logger.info("Compare File >>> " + file_section)
        test = CompareGEDFZipFile(file_section)
        test.init_param(section_name)
        test.test()

    # 从得到的结果集中找到所有的DataId,用来查看比较文件中的DataId
    def get_all_dataId(self, set_r):
        set_d = set()
        for r in set_r:
            if r:
                set_d.add(r.split("|")[self.dataId_index])
        return set_d


if __name__ == '__main__':
    # 用来解析zip文件中的Id
    # file = "D:\QA\GEDF\MOCAL5267_Fin_EarReport\GEDF\NRA\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-05-24.zip"
    # data = Test.read_id_from_zip(file)
    # print data

    CompareGEDFZipFile.batch_test('MOCAL5284_Delta_NRA_Fundamental_FinancialStatements')
    # CompareGEDFZipFile.single_test("MOCAL5280_Delta_UKI_OwnershipDetails")
    # CompareGEDFZipFile.single_test("MOCAL5319_Delta_NRA_FinancialStatementsRestate")
