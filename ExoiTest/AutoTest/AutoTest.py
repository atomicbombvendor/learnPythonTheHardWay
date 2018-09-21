# coding=utf-8
import codecs
import datetime
import os
import re

from ExoiTest import myglobal
from ExoiTest.CompareExoi.ExoiEntry import multi_process
from ExoiTest.CompareGEDFZipFile.CompareGEDFZipFile import CompareGEDFZipFile
from ExoiTest.GenerateTestCaseBat.GenerateTestCase import generate_branch_bat
import ConfigParser

parser = ConfigParser.ConfigParser()
parser.read("../ConfigFile/AutoTest.ini")
section_p = parser.get("AutoTest", "section_test")
CompareZip_File_Config = parser.get("AutoTest", "CompareZip_File_Config")
GenerateBat_config = parser.get("AutoTest", "GenerateBat_config")
CompareExoi_Config = parser.get("AutoTest", "CompareExoi_Config")
logger = myglobal.get_logger()


# 从配置文件中读取必要的节点信息，返回dict
def read_config():
    global GenerateBat_config
    config_value = {}
    c_parser = ConfigParser.ConfigParser()
    c_parser.read(GenerateBat_config)
    config_value["root"] = c_parser.get(section_p, "Root")
    config_value["master"] = c_parser.get(section_p, "Master")
    config_value["new_branch"] = c_parser.get(section_p, "New_Branch")
    config_value["master_zip_file"] = c_parser.get(section_p, "Master_ZipFile")
    config_value["new_branch_zip_file"] = c_parser.get(section_p, "New_branch_ZipFile")
    config_value["file_name"] = c_parser.get(section_p, "FileName").split(",")
    config_value["target_file_date"] = c_parser.get(section_p, "TargetFileDate")
    config_value['data_id_index'] = c_parser.get(section_p, "DataIdIndex")

    config_value["section_title"] = section_p.split("_")[0]
    config_value["root_master"] = config_value["master"] + "\\" + config_value["master_zip_file"]
    config_value["root_new_branch"] = config_value["new_branch"] + "\\" + config_value["new_branch_zip_file"]
    config_value["file_names"] = config_value["file_name"].split(",") if "," in config_value["file_name"] \
        else config_value["file_name"]
    config_value["target_file_date_d"] = datetime.datetime.strptime(config_value["target_file_date"], '%Y-%m-%d')
    config_value["monthly_file_date"] = "%s-%s" % (str(config_value["target_file_date_d"].year),
                                                   str(config_value["target_file_date_d"].month - 1))
    config_value["daily_delta_file_date"] = config_value["target_file_date"]

    return config_value


# 生成测试bat
def generate_testCase():
    generate_branch_bat(1, section_p)  # 生成master测试bat
    generate_branch_bat(2, section_p)  # 生成新分支测试bat


# 检索zip文件路径，写入 ../ConfigFile/CompareZip_File_Config.ini
def write_CompareGEDFZipFile_ini():
    global CompareZip_File_Config
    config_value = read_config()

    zip_path_content = {}
    for file_name in config_value["file_names"]:
        tmp = find_targetZipFile(config_value["root_new_branch"], file_name, config_value["monthly_file_date"],
                                 config_value["daily_delta_file_date"])
        zip_path_content.update(tmp)
    ZipFile_TestCase_Content = generate_compare_Zip_Content(zip_path_content, config_value)

    for content in ZipFile_TestCase_Content:
        write_content(CompareZip_File_Config, content)
    logger.info("Write Zip File Path into " + CompareZip_File_Config)


# 检索比较的文件文件路径，写入 ../ConfigFile/CompareExoi_File_Config.ini
def write_CompareExoi_ini():
    zip_diff = find_zip_diff()
    zip_diff_content = generate_zip_diff_content(zip_diff)
    for content in zip_diff_content:
        write_content(CompareExoi_Config, content)
    logger.info("Write Compare Result File Path into " + CompareExoi_Config)


# 根据指定的 file_name 找出所有的文件，返回dict
def find_targetZipFile(root_path, file_name, monthly_fileDate, daily_delta_fileDate):
    result = {}

    for root, dirs, files in os.walk(root_path, topdown=False):
        for f in files:
            if file_name in f and (monthly_fileDate in f or daily_delta_fileDate in f) and 'zip' in f and 'Outputs' not in root:
                path = os.path.join(root, f)

                # 正则表达式分组用(?P<name>正则表达式)#name是一个合法的标识符
                pattern = r"(\\(?P<bigtype>Deadwood|DOW30|FTSE100)|(?P<bigtype2>))\\(?P<region>[a-zA-Z_\s]+?)\\(" \
                          r"?P<package>[a-zA-Z_0-9]+?)\\(?P<fileType>.+?)\\(?P<schedule>Monthly|Daily|Delta)\\(" \
                          r"?P<file>.*?)\.zip"
                res = re.search(pattern, path.replace(root_path, ""))
                try:
                    big_type = res.group('bigtype')
                except AttributeError, e:
                    big_type = None
                region = res.group('region')
                schedule = res.group('schedule')
                package = res.group('package')
                file_type = file_name
                key = "%s_" % big_type if big_type else ''
                key += '%s_%s_%s_%s' % (schedule, region, package, file_type)
                logger.info("Find Zip File: " + path.replace(root_path, ""))
                result[key] = path.replace(root_path, "")
                '''
                (?P<bigtype>Deadwood|DOW30|FTSE100)\\\\(?P<region>[A-Z]{3})\\\\.*?\\\\(?P<fileType>[A-Z]+)\\\\(?P<schedule>Monthly|Daily|Delta)\\\\(?P<file>.*?)\.zip
                '''
    return result


# 得到路径:比较压缩包得到的不同文件的
def find_zip_diff():
    global CompareExoi_Config
    config_value = read_config()

    root_new_branch = "%s\\Result" % config_value["new_branch"]
    zip_diff = {}
    for root, dirs, files in os.walk(root_new_branch, topdown=True):
        for dir_t in dirs:
            zip_diff[dir_t] = os.path.join(root, dir_t)
    return zip_diff


# 生成测试用例内容，放在CompareZip_File_Config.ini文件中
# 格式
# [@section@_@key@]
# source_master = @root_master@@zip_path@
# source_new_branch =  @root_new_branch@@zip_path@
# result = @root_new_branch2@[:-4]Result
# dataId_index = @index@
def generate_compare_Zip_Content(zip_dict, config_value):
    template = "\r\n\r\n[@section@_@key@]\r\nsource_master = @root_master@@zip_path@\r\nsource_new_branch =  " \
               "@root_new_branch@@zip_path@\r\nresult = @root_new_branch2@Result\r\ndataId_index = 1"
    ZipFile_TestCase_Content = []
    for k, v in zip_dict.items():
        content = template.replace("@section@", config_value["section_title"])
        content = content.replace("@key@", k)
        content = content.replace("@root_master@", config_value["root_master"])
        content = content.replace("@root_new_branch@",  config_value["root_new_branch"])
        content = content.replace("@root_new_branch2@",  config_value["root_new_branch"][:-4])
        content = content.replace("@zip_path@", v)
        content = content.replace("@index@", config_value['data_id_index'])

        ZipFile_TestCase_Content.append(content)

    return ZipFile_TestCase_Content


# 生成测试用例内容，放在CompareExoi_File_Config.ini文件中
# 格式
# [@dict_key@]
# source_file = @dict_value@\\new_diff.dat
# target_file = @dict_value@\\a.dat
def generate_zip_diff_content(zip_diff_dict):
    content_arr = []
    template = "\r\n[@dict_key@]\r\nsource_file = @dict_value@\\new_diff.dat\r\ntarget_file = @dict_value@\\a.dat\r\n"
    for k, v in zip_diff_dict.items():
        content = template.replace("@dict_key@", k)
        content = content.replace("@dict_value@", v)
        content = content.replace("@dict_value@", v)
        content_arr.append(content)
    return content_arr


def write_content(target_file, content):
    section_c = re.search("\[(?P<section>[A-Za-z_0-9]+?)\]", content, re.S).group("section")
    m_parser = ConfigParser.ConfigParser()
    m_parser.read(target_file)
    if not m_parser.has_section(section_c):
        with codecs.open(target_file, "a+", "utf-8") as f:
            f.write(content)


# 修改logger配置文件的内容
def modify_log_file_name(file_name):
    content = ""
    log_file = "../resource/logconfig.conf"
    with codecs.open(log_file, "r", "utf-8") as f:
        for line in f:
            if "log_file" in line:
                content += "log_file = d:/QA/Log/exoi_%s_@time@.txt\r\n" % (file_name)
            else:
                content += line

    with codecs.open(log_file, "wb", "utf-8") as f:
        f.write(content)


# 自动化测试入口
def auto_test():
    section_title = section_p.split("_")[0] + "_"
    modify_log_file_name(section_title)

    write_CompareGEDFZipFile_ini()
    CompareGEDFZipFile.batch_test(section_title)
    write_CompareExoi_ini()
    # compare exoi
    multi_process(section_title)


if __name__ == "__main__":
    auto_test()
