# coding=utf-8
import codecs
import gzip
import zipfile

import os


class Test:

    def __init__(self):
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\UKI\Ownership\MonthEndInstitution\Monthly\Monthly_MonthEndInstitution_2017-12.zip'
        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\UKI\Ownership\OwnershipSummary\Monthly\Monthly_OwnershipSummary_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\Result\UKI'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\FTSE100\UKI\Ownership\OwnershipSummary\Monthly\Monthly_OwnershipSummary_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\FTSE100\UKI\Ownership\MonthEndInstitution\Monthly\Monthly_MonthEndInstitution_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\Result\FTSE'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\DOW30\NRA\Ownership\OwnershipSummary\Monthly\Monthly_OwnershipSummary_2017-12.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\DOW30\NRA\Ownership\MonthEndInstitution\Monthly\Monthly_MonthEndInstitution_2017-12.zip'
        # self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\Result\DOW30'

        # self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\UKI\Ownership\OwnershipSummary\Delta\Delta_OwnershipSummary_2018-01-22.zip'
        # self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4202\GeDataFeed\UKI\Ownership\MonthEndInstitution\Delta\Delta_MonthEndInstitution_2018-01-22.zip'
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

        self.uki_source_old = 'D:\QA\GEDF\GEDataFeed-master\GEDF\Deadwood\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsRestate_2017-12.zip'
        self.uki_source_new = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\GEDF\Deadwood\UKI\Fundamental\FinancialStatements\Monthly\Monthly_FinancialStatementsRestate_2017-12.zip'
        self.uki_result = 'D:\QA\GEDF\GEDataFeed-MOCAL4807\Result\DeadwoodUKIFundamental\FinancialStatementsMonthly\Restate'

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
    def write_file(self, old, new, path, old_result_file, new_result_file):
        if not os.path.exists(path):
            os.mkdir(path)
        with codecs.open(old_result_file, 'w', 'utf-8') as fnl:
            for line in list(old):
                fnl.write(str(line)+"\r\n")
        with codecs.open(new_result_file, 'w', 'utf-8') as fnd:
            for line in list(new):
                fnd.write(str(line)+"\r\n")

    def test(self):
        result_old = self.uki_result + '\old_diff.dat'
        result_new = self.uki_result + '\\new_diff.dat'
        file_data_old = self.testZip(self.uki_source_old)
        file_data_new = self.testZip(self.uki_source_new)

        set_old = self.get_set(file_data_old)
        set_new = self.get_set(file_data_new)

        # set_old是标准文件，set_new是新产生的文件
        # diff_old是只在old中存在的； diff_new 是只在新文件中存在的
        diff_old, diff_new = self.compareFiles(set_old, set_new)

        self.write_file(diff_old, diff_new, self.uki_result, result_old, result_new)


if __name__ == '__main__':
    T = Test()
    T.test()

