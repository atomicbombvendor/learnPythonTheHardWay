# coding=utf-8
import codecs
import os
import re
import ConfigParser

section = ""


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
        pass
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
# replace不会修改字符串的值
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
    # ft = "/IDList="
    # if ft not in content:
    #     content += ft + idList
    # return content
    return content


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
    config.read("../ConfingFile/GenerateBat_config.ini")

    if 1 == branch_flag:
        branch_name = "master"
    elif 2 == branch_flag:
        branch_name = "new_branch"
    files = getAllFiles(config)
    bat_folder = config.get(section, "bat_folder")
    branch = config.get(section, branch_name)
    branch_ZipFile = config.get(section, branch_name + "_ZipFile")

    for bat in files:
        with codecs.open(bat, "r", "utf-8") as F:
            file_name = os.path.basename(F.name)
            processed_content = updateBatContent(F.read(), file_name, config, branch, branch_ZipFile)
            target_bat = branch + "\\" + bat_folder + "\\" + file_name
            write_file(target_bat, processed_content)
    print("Bat Path>>>" + branch + "\\" + bat_folder)


if __name__ == "__main__":
    section_p = "5177_Testcase"
    generate_branch_bat(1, section_p)
    generate_branch_bat(2, section_p)
