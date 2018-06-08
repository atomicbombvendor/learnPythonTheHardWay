# coding=utf-8
import datetime

from ExoiTest.GenerateTestCaseBat.GenerateTestCase import generate_branch_bat
import ConfigParser


# 从配置文件中读取必要的节点信息，用来找到对应的Zip文件
def read_config(section_p):
    config_value = {}
    parser = ConfigParser.ConfigParser()
    parser.read("../CompareGEDFZipFile/MOCAL_File_Config.ini")
    config_value["root"] = parser.get(section_p, "root")
    config_value["master"] = parser.get(section_p, "master")
    config_value["new_branch"] = parser.get(section_p, "new_branch")
    config_value["master_ZipFile"] = parser.get(section_p, "master_ZipFile")
    config_value["new_branch_ZipFile"] = parser.get(section_p, "new_branch_ZipFile")
    config_value["FileName"] = parser.get(section_p, "new_branch_ZipFile").split(",")
    config_value["TargetFileDate"] = parser.get(section_p, "TargetFileDate")


# 生成测试bat
def generate_testCase(section_p):
    generate_branch_bat(1, section_p)  # 生成master测试bat
    generate_branch_bat(2, section_p)  # 生成新分支测试bat


# 检索zip文件路径，写入 ../CompareGEDFZipFile/MOCAL_File_Config.ini
def write_CompareGEDFZipFile_ini(section_p):
    config_values = read_config(section_p)
    source_zip_root_path = config_values["master"] + "\\" + config_values["master_ZipFile"]
    new_branch_zip_root_path = config_values["new_branch"] + "\\" + config_values["new_branch_ZipFile"]
    file_names = config_values["FileName"]
    targetFileDate = datetime.datetime.strptime(config_values["TargetFileDate"], '%Y-%m-%d')
    monthly_fileDate = str(targetFileDate.year) + "-" + str(targetFileDate.month-1)
    daily_delta_fileDate = config_values["TargetFileDate"]

    # 从新分支的zip路径下找到所有的符合FileType和Date的ZIP包路径
    # 拼接出section {Jira}_{schedule}{_Deadwood|DOW30|FTSE100}_{Region}_{FileName}
    # 根据路径拼接出完整的Template
    # 写入（append）../CompareGEDFZipFile/MOCAL_File_Config.ini中




