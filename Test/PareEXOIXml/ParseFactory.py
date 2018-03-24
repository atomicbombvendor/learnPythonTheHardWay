# coding=utf-8
from Test.PareEXOIXml.Parse.EXOIParseFinancialStatement import *


class ParseFactory:

    def __init__(self):
        pass

    def get_Exoi_Type(self, content):

        class_name = {
            # 返回类名
            'EXOIParseFinancialStatement': EXOIParseFinancialStatement
        }
        if class_name[content]:
            return class_name[content]()
        else:
            print "没有类名为", content, " 请检查输入！"
