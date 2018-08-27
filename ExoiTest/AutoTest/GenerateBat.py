# coding=utf-8
import ConfigParser

from ExoiTest.GenerateTestCaseBat.GenerateTestCase import generate_branch_bat

parser = ConfigParser.ConfigParser()
parser.read("../ConfigFile/AutoTest.ini")
section_p = parser.get("AutoTest", "section_test")


# 生成测试bat
# 根据配置在AutoTest.ini中的节点，找到要修改的Bat文件信息
def generate_testCase():
    generate_branch_bat(1, section_p)  # 生成master测试bat
    generate_branch_bat(2, section_p)  # 生成新分支测试bat


if __name__ == "__main__":
    generate_testCase()