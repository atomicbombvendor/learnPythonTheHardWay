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

        self.source_old = self.conf.get(sectionName, 'source_old')
        self.source_new = self.conf.get(sectionName, 'source_new')
        self.result = self.conf.get(sectionName, 'result')
         
        # region 以前的测试 折叠起来了
        # MOCAL 4204 UKI
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4204\GEDF\UKI\Ownership\OwnershipMonthlySummary\Monthly\Monthly_OwnershipMonthlySummary_2017-11.zip'
        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4204\GEDF\UKI\Ownership\OwnershipSummary\Monthly\Monthly_OwnershipSummary_2017-11.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4204\Result\UKI'
        #
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4204\GEDF\UKI\Ownership\OwnershipMonthlySummary\Monthly\Monthly_OwnershipMonthlySummary_0P00007OUP_2017-11.zip'
        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4204\GEDF\UKI\Ownership\OwnershipSummary\Monthly\Monthly_OwnershipSummary_0P00007OUP_2017-11.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4204\Result\UKI\\file'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\FTSE100\UKI\Ownership\OwnershipSummary\Monthly\Monthly_OwnershipSummary_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\FTSE100\UKI\Ownership\MonthEndInstitution\Monthly\Monthly_OwnershipMonthlySummary_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\Result\FTSE'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\DOW30\NRA\Ownership\OwnershipSummary\Monthly\Monthly_OwnershipSummary_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\DOW30\NRA\Ownership\MonthEndInstitution\Monthly\Monthly_OwnershipMonthlySummary_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\Result\DOW30'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\UKI\Ownership\OwnershipSummary\Delta\Delta_OwnershipSummary_2018-01-22.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\UKI\Ownership\MonthEndInstitution\Delta\Delta_OwnershipMonthlySummary_2018-01-22.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\Result\Delta\DOW30'

        # MOCAL 4807
        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\NRA\Fundamental\EarningReports\Monthly\Monthly_EarningReportsAOR_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\NRA\Fundamental\EarningReports\Monthly\Monthly_EarningReportsAOR_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\NRAFundamental\EarningReportsMonthly\AOR'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\NRA\Fundamental\EarningReports\Monthly\Monthly_EarningReportsRestate_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\NRA\Fundamental\EarningReports\Monthly\Monthly_EarningReportsRestate_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\NRAFundamental\EarningReportsMonthly\Restate'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\NRA\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsAOR_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\NRA\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsAOR_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\NRAFundamental\FinancialStatementsMonthly\AOR'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\NRA\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsRestate_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\NRA\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsRestate_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\NRAFundamental\FinancialStatementsMonthly\Restate'
        # Deadwood UKI
        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\Deadwood\UKI\Fundamental\EarningReports\Monthly\Monthly_EarningReportsAOR_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\Deadwood\UKI\Fundamental\EarningReports\Monthly\Monthly_EarningReportsAOR_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\DeadwoodUKIFund amental\EarningReportsMonthly\AOR'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\Deadwood\UKI\Fundamental\EarningReports\Monthly\Monthly_EarningReportsRestate_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\Deadwood\UKI\Fundamental\EarningReports\Monthly\Monthly_EarningReportsRestate_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\DeadwoodUKIFundamental\EarningReportsMonthly\Restate'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\Deadwood\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsAOR_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\Deadwood\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsAOR_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\DeadwoodUKIFundamental\FinancialStatementsMonthly\AOR'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\Deadwood\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsRestate_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\Deadwood\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsRestate_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\DeadwoodUKIFundamental\FinancialStatementsMonthly\Restate'

        # MOCAL-4517
        # DOW30 EarningRatiosAOR
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\DOW30\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\DOW30\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\DOW30\EarningRatiosAOR"

        # DOW30 EarningRatiosRestate
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\DOW30\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\DOW30\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\DOW30\EarningRatiosRestate"

        # FTSE EarningRatiosAOR
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\FTSE100\UKI\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\FTSE100\UKI\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\FTSE100\EarningRatiosAOR"

        # FTSE EarningRatiosRestate
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\FTSE100\UKI\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\FTSE100\UKI\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\FTSE100\EarningRatiosRestate"

        # NRA EarningRatiosAOR
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\NRA\EarningRatiosAOR"

        # NRA EarningRatiosRestate
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\NRA\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\NRA\EarningRatiosRestate"

        # EUR EarningRatiosAOR
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\EUR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\EUR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\EUR\EarningRatiosAOR"

        # EUR EarningRatiosRestate
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\EUR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\EUR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\EUR\EarningRatiosRestate"

        # Deadwood AFR EarningRatiosAOR
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\Deadwood\AFR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\Deadwood\AFR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosAOR_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\Deadwood\EarningRatiosAOR"

        # Deadwood AFR EarningRatiosRestate
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\Deadwood\AFR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\Deadwood\AFR\Fundamental\EarningRatios\Monthly\Monthly_EarningRatiosRestate_2017-11.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\Deadwood\EarningRatiosRestate"

        # Delta FD EarningRatiosAOR
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\Delta\AFR\Fundamental\EarningRatios\Delta\Delta_EarningRatiosAOR_2017-12-12.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\Delta\AFR\Fundamental\EarningRatios\Delta\Delta_EarningRatiosAOR_2017-12-12.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\Delta\EarningRatiosAOR"

        # Delta FD EarningRatiosRestate
        # self.uki_source_old = "D:\QA\GEDF\GEDataFeed-master\GEDF\Delta\AFR\Fundamental\EarningRatios\Delta\Delta_EarningRatiosRestate_2017-12-12.zip"
        # self.uki_source_new = "D:\QA\GEDF\GEDataFeed-MOCAL4517\GEDF\Delta\AFR\Fundamental\EarningRatios\Delta\Delta_EarningRatiosRestate_2017-12-12.zip"
        # self.uki_result = "D:\QA\GEDF\GEDataFeed-MOCAL4517\Result\Delta\EarningRatiosRestate"
        # region2 折叠起来了

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
        file_data_old = self.testZip(self.source_old)
        file_data_new = self.testZip(self.source_new)

        set_old = self.get_set(file_data_old)
        set_new = self.get_set(file_data_new)

        # set_old是标准文件，set_new是新产生的文件
        # diff_old是只在old中存在的； diff_new 是只在新文件中存在的
        diff_old, diff_new = self.compareFiles(set_old, set_new)

        self.write_file(diff_old, diff_new, self.result, result_old, result_new)
        print "文件比对结束"


if __name__ == '__main__':
    # MOCAL4722_DOW30_AOR = "MOCAL4722_DOW30_AOR"
    # MOCAL4722_DOW30_Restate = "MOCAL4722_DOW30_Restate"
    # MOCAL4722_FTSE100_AOR = "MOCAL4722_FTSE100_AOR"
    # MOCAL4722_FTSE100_Restate = "MOCAL4722_FTSE100_Restate"
    # file_section = "MOCAL4892_Delta_NRA_FinancialStatements_AOR"
    # print "Compare File >>>", file_section
    # T = Test(file_section)
    # T.test()

    # 用来解析zip文件中的Id
    # file = "D:\QA\GEDF\GeDataFeed-MOCAL4937\GEDF\FTSE100\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsAOR_2018-2.zip"
    # data = T.read_id_from_zip(file)
    # print data

    # 读取配置文件中的和某个关键字有关的Section
    conf = ConfigParser.ConfigParser()
    conf.read('MOCAL_File_Config.ini')
    file_sections = conf.sections()
    for section in file_sections:
        if 'MOCAL4892' in section:
            print "Compare File >>>", section
            T = Test(section)
            T.test()
