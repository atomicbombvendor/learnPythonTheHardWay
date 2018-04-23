# coding=utf-8
import codecs
import ConfigParser
from ExoiTest.PareEXOIXml.ParseFactory import *


class StartParse:

    # 每次处理一个文件是，type和参数都是一样的（需要把Date的范围扩到最大）
    def __init__(self, file_type_):
        self.exoi_type = ParseFactory().get_Exoi_Type(file_type_)
        self.not_match = []
        self.do_match = []

    def start_parse(self, universe_param, file_path = ""):
        self.exoi_type.construct_full_param(universe_param)
        self.exoi_type.get_content()  # 调用父类方法,先登录,然后从URL中获取XML内容
        flag = self.exoi_type.start_parse(file_path)  # 把获取的XML内容转换为文件形式
        if not flag:
            print("转换成功")
        else:
            print("转换不成功")


if __name__ == '__main__':
    file_type = 'EXOIParseFinancialStatement'
    # MOCALFile_Section = '4973_EarningReport_UKI_Restate'
    # conf = ConfigParser.ConfigParser()
    # conf.read('MOCAL_File_Config.ini')
    # source_file = conf.get(MOCALFile_Section, 'source_file')
    # target_file = conf.get(MOCALFile_Section, 'target_file')
    # print "Verify File ***********" + MOCALFile_Section
    test = StartParse(file_type)
    # test.test(line_value)
    universe_param = {
        "Id": "0C00000W54",
        "IdType": "CompanyId",
        "ReportType": "A",
        "Year": "2017,2016"
    }
    test.start_parse(universe_param)