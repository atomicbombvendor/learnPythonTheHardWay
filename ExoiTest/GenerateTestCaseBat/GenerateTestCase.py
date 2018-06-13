# coding=utf-8
import codecs
import os
import re
import ConfigParser

from lxml import etree

from ExoiTest import myglobal

section = ""
logger = myglobal.get_logger()


# 从root中得到所有的文件
def getAllFiles(config):
    root_path = config.get(section, "root")
    bat_files = []
    for root, dirs, files in os.walk(root_path, topdown=False):
        for file_b in files:
            bat_files.append(os.path.join(root, file_b))
    return bat_files


def updateBatContent(content, filename, config, branch_root, branch_ZipFile):
    file_type = config.get(section, "FileType")
    id_list = config.get(section, "IdList")
    targetFileDate = config.get(section, "TargetFileDate")
    content = replace_exe_path(content, branch_root)

    if "Deadwood" in filename:
        content = replace_file_type(content, file_type)
        content = add_idList(content, id_list)
    elif "DOW30" in filename or "FTSE100" in filename:
        content = replace_file_type(content, file_type)
    elif "Delta" in filename:
        update_message_share_folder(branch_root, config.get(section, "Message_ShareFolder"))
        update_running_job_host(branch_root, config.get(section, "RunningDeltaJobsHost"))
    else:
        content = replace_file_type(content, file_type)
        content = add_idList(content, id_list)

    content = replace_output_file(content, branch_root, branch_ZipFile)
    content = replace_zip_file(content, branch_root, branch_ZipFile)
    content = update_targetFileDate(content, targetFileDate)
    return content


def replace_exe_path(content, root):
    if "D:\GEDataFeed\GeDataFeed_Monthly\\bin\EquityDataFeed.exe" in content:
        content = content.replace("D:\GEDataFeed\GeDataFeed_Monthly\\bin\EquityDataFeed.exe",
                                  root + "\GeDataFeed_Monthly\\bin\EquityDataFeed.exe")

    if "D:\GEDataFeed\GeDataFeed_Daily\\bin\EquityDataFeed.exe" in content:
        content = content.replace("D:\GEDataFeed\GeDataFeed_Daily\\bin\EquityDataFeed.exe",
                                  root + "\GeDataFeed_Daily\\bin\EquityDataFeed.exe")

    if "D:\GEDataFeed\GeDataFeed_Delta\\bin\EquityDataFeed.exe" in content:
        content = content.replace("D:\GEDataFeed\GeDataFeed_Delta\\bin\EquityDataFeed.exe",
                                  root + "\GeDataFeed_Delta\\bin\EquityDataFeed.exe")

    return content


# 不区分 DOW30 Deadwood FTSE100 和正常的Region 以及Delta
# replace不会修改原字符串的值，会返回修改后的字符串
def replace_file_type(content, FileType):
    ft = "/FileType=(.+?)/"  # 要匹配的值find_target
    s_old = re.search(ft, content, re.S).group(0)  # 修改前的值
    s_new = ft.replace("(.+?)", FileType + " ")  # 要修改后的值
    return content.replace(s_old, s_new)


def replace_zip_file(content, root, ZipFile):
    ft = "/ZipFilesDir=\\\\morningstar.com\shares\GeDataFeed\GeDataFeed"  # 有一些带有后缀的路径，DOW30
    s_new = "/ZipFilesDir=" + root + "\\" + ZipFile
    if "/ZipFilesDir=" in content:  # 如果存在这个值
        content = content.replace(ft, s_new)
    else:
        content += " " + s_new
    return content


def replace_output_file(content, root, outputs):
    ft = "/OutputDir=D:\GEDataFeed\Outputs"
    s_new = "/OutputDir=" + root + "\\" + outputs + "\\Outputs"
    if "/OutputDir=" in content:  # 如果存在这个值
        content = content.replace(ft, s_new)
    else:
        content += " " + s_new
    return content


def add_idList(content, idList):
    ft = " /IDList=%s "
    if ft not in content:
        content += ft % idList
    return content


# only for delta config file
# xpath: configuration\appSettings\add[@key='Message_ShareFolder']
def update_message_share_folder(root_path, message_share_folder):
    xml_file = "%s\\GeDataFeed_Delta\\bin\EquityDataFeed.exe.config" % root_path
    xml_output_file = "%s\\GeDataFeed_Delta\\bin\EquityDataFeed.exe.config" % root_path
    tree = etree.parse(xml_file)
    path = "/configuration/appSettings/add[@key='Message_ShareFolder']"
    target_node = tree.xpath(path)
    for node in target_node:
        if 'Message_ShareFolder' in node.attrib['key']:
            node.attrib['value'] = message_share_folder

    tree.write(xml_output_file, encoding='utf-8', xml_declaration=True)


def write_xml(tree, out_path):
    '''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


# only for delta config file
# xpath: configuration\appSettings\add[@key='RunningDeltaJobsHost']
def update_running_job_host(root_path, running_job_host):
    xml_file = "%s\\GeDataFeed_Delta\\bin\EquityDataFeed.exe.config" % root_path
    xml_output_file = "%s\\GeDataFeed_Delta\\bin\EquityDataFeed.exe.config" % root_path
    tree = etree.parse(xml_file)
    path = "/configuration/appSettings/add[@key='RunningDeltaJobsHost']"
    target_node = tree.xpath(path)
    for node in target_node:
        if 'RunningDeltaJobsHost' in node.attrib['key']:
            node.attrib['value'] = running_job_host

    tree.write(xml_output_file, encoding='utf-8', xml_declaration=True)


def update_targetFileDate(content, targetFileDate):
    ft = "/TargetFileDate=%1"
    s_new = "/TargetFileDate=" + targetFileDate
    if "/TargetFileDate=" in content:  # 如果存在这个值
        content = content.replace(ft, s_new)
    else:
        content += " " + s_new
    return content


def write_file(file_t, content):
    folder_path = os.path.dirname(file_t)
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

    with codecs.open(file_t, "w+", "utf-8") as f:
        f.write(content)


# 生成bat文件
# branch_flag = 1 生成master分支的bat文件
# branch_flag = 2 生成新分支的bat文件
def generate_branch_bat(branch_flag, section_p):
    global section
    section = section_p
    global branch_name
    config = ConfigParser.ConfigParser()
    config.read("../ConfigFile/GenerateBat_config.ini")

    if 1 == branch_flag:
        branch_name = "master"
    elif 2 == branch_flag:
        branch_name = "new_branch"
    files = getAllFiles(config)
    bat_folder = config.get(section, "Bat_Folder")
    branch = config.get(section, branch_name)
    branch_ZipFile = config.get(section, branch_name + "_ZipFile")

    for bat in files:
        with codecs.open(bat, "r", "utf-8") as F:
            file_name = os.path.basename(F.name)
            processed_content = updateBatContent(F.read(), file_name, config, branch, branch_ZipFile)
            target_bat = branch + "\\" + bat_folder + "\\" + file_name
            write_file(target_bat, processed_content)
    logger.info("Generate Bat Path>>>%s\\%s, Please Run Bat!" % (branch, bat_folder))


if __name__ == "__main__":
    section_p = "5177_Testcase"
    generate_branch_bat(1, section_p)
    generate_branch_bat(2, section_p)
