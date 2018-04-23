# coding=utf-8
import codecs
import gzip
import re
import zipfile
import ConfigParser
import os


class Test:

    def __init__(self, sectionName):

        self.conf = ConfigParser.ConfigParser()
        self.conf.read('MOCAL_File_Config.ini')

        self.source_master = self.conf.get(sectionName, 'source_master')
        self.source_new_branch = self.conf.get(sectionName, 'source_new_branch')
        self.result = self.conf.get(sectionName, 'result') + "\\" + sectionName
        dataId_index_t = self.conf.get(sectionName, 'dataId_index')  # 用来确定DataId所在的位置, 默认为1
        self.dataId_index = int(dataId_index_t) if dataId_index_t else 1

    # 读取压缩文件，返回压缩文件内的文件
    def read_gz_file(self, file):
        if os.path.exists(file):
            with gzip.open(file, 'r') as pf:
                for line in pf:
                    yield line
        else:
            print('the path [{}] is not exist!'.format(file))

    def testZip(self, file):
        zfile = zipfile.ZipFile(file, 'r')
        data = ''
        for filename in zfile.namelist():
            data += zfile.read(filename)
        return data

    def read_id_from_zip(self, file):
        zfile = zipfile.ZipFile(file, 'r')
        pattern = r"(0P[0-9A-Za-z]{8}|0C[0-9A-Za-z]{8})"
        data = ''
        for filename in zfile.namelist():
            match = re.search(pattern, filename)
            if match:
                data += match.group()+"\r\n"
        return data

    # 把data放入set中
    def get_set(self, data):
        result = set()
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
            print("Old is not null ")
            print("DataIds in old>> " + " ".join(self.get_all_dataId(old)))
        else:
            print("Old is null ")
        if len(list(new)) > 0:
            print("new is not null ")
            print("DataIds in new>> " + " ".join(self.get_all_dataId(new)))
        else:
            print("new is null ")

        if not os.path.exists(path):
            os.makedirs(path)  # 创建级联目录
        with codecs.open(old_result_file, 'w', 'utf-8') as fnl:
            for line in list(old):
                fnl.write(str(line)+"\r\n")
        with codecs.open(new_result_file, 'w', 'utf-8') as fnd:
            for line in list(new):
                fnd.write(str(line)+"\r\n")

    def test(self):
        result_old = self.result + '\old_diff.dat'
        result_new = self.result + '\\new_diff.dat'
        file_data_old = self.testZip(self.source_master)
        file_data_new = self.testZip(self.source_new_branch)

        set_old = self.get_set(file_data_old)
        set_new = self.get_set(file_data_new)

        # set_old是标准文件，set_new是新产生的文件
        # diff_old是只在old中存在的； diff_new 是只在新文件中存在的
        diff_old, diff_new = self.compareFiles(set_old, set_new)
        self.write_file(diff_old, diff_new, self.result, result_old, result_new)
        print "文件比对结束\r\n"

    # 读取配置文件中的和某个关键字有关的Section, 然后比较所有的文件
    @staticmethod
    def batch_test(section_num_name):
        conf = ConfigParser.ConfigParser()
        conf.read('MOCAL_File_Config.ini')
        file_sections = conf.sections()
        for section in file_sections:
            if section_num_name in section:
                print "Start Compare File >>>", section
                T = Test(section)
                T.test()

    # 读取配置文件中和section_name匹配的Section, 然后比较文件
    @staticmethod
    def single_test(section_name):
        file_section = section_name
        print "Compare File >>>", file_section
        T = Test(file_section)
        T.test()

    # 从得到的结果集中找到所有的DataId,用来查看比较文件中的DataId
    def get_all_dataId(self, set_r):
        set_d = set()
        for r in set_r:
            if r:
                set_d.add(r.split("|")[self.dataId_index])
        return set_d


if __name__ == '__main__':
    # 用来解析zip文件中的Id
    # file = "D:\QA\GEDF\GeDataFeed-MOCAL4937\GEDF\FTSE100\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsAOR_2018-2.zip"
    # data = T.read_id_from_zip(file)
    # print data

    Test.batch_test('MOCAL5058')

