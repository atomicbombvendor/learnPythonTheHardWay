# coding=utf-8

# 要比较产生的文件，分给两种
# 第一层 Reference_v2 Reference_v3
# 第二层 SecurityReference/Daily/Daily_SecurityReference_2018_05-03.zip
#       SecurityReference/Monthly/Monthly_SecurityReference_2018_4.zip
#       CompanyReference/Monthly/Monthly_CompanyReference_2018_4.zip
#       CompanyReference/Monthly/Monthly_CompanyReference_2018_4.zip
# 加上 Region
# Reference_v2 下面只能有1006和1007的点，拒绝1008
# Reference_v3 下面只能有1007的点
# 首先，判断这些文件存不存在；然后找出这些文件的点 1006 1007 1008
import gzip
import logging
import os
import string
import sys
import zipfile

regions = {
    'AFR',
    'Deadwood\AFR',
    'ANZ',
    'Deadwood\ANZ',
    'ASP',
    'Deadwood\ASP',
    'EUR',
    'Deadwood\EUR',
    'IPM',
    'Deadwood\IPM',
    'LTA',
    'Deadwood\LTA',
    'NRA',
    'Deadwood\NRA',
    'UKI',
    'Deadwood\UKI'
}

Reference = {'Reference_v2', 'Reference_v3'}

file = {
    '@Region@\@Rf@\CompanyReference\Daily\Daily_CompanyReference_2018-05-03.zip',
    '@Region@\@Rf@\CompanyReference\Monthly\Monthly_CompanyReference_2018-4.zip',
    '@Region@\@Rf@\SecurityReference\Daily\Daily_SecurityReference_2018-05-03.zip',
    '@Region@\@Rf@\SecurityReference\Monthly\Monthly_SecurityReference_2018-4.zip'
}


log_filename = "t4724_log.log"
logger = logging.getLogger(__name__)
# filter = logging.Filter(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')

file_handler = logging.FileHandler(log_filename, mode='a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# file_handler.addFilter(filter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
# file_handler.addFilter(filter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def file_exists(root):
    if not root.endswith("\\"):
        root = root + "\\"
    for rf in Reference:
        for region in regions:
            for f in file:
                tmp_file = root + f.replace('@Region@', region).replace('@Rf@', rf)

                if "CompanyReference" in tmp_file:
                    data_id_index = 1
                else:
                    data_id_index = 2

                if os.path.exists(tmp_file):
                    dataIds = get_all_dataId(read_Zip(tmp_file), data_id_index)
                    logger.info(tmp_file.replace(root, "") + " data id:\n" + string.join(dataIds, ", "))
                    if "SecurityReference" in tmp_file and "Reference_v2" in tmp_file:
                        if ("1006" in dataIds) and ("1007" in dataIds) and ("1008" not in dataIds):
                            logger.info("V2 DataId Correct\n")
                        else:
                            logger.error("V2 DataId NotCorrect\n")

                    if "SecurityReference" in tmp_file and "Reference_v3" in tmp_file:
                        if ("1006" not in dataIds) and ("1007" in dataIds) and ("1008" not in dataIds):
                            logger.info("V3 DataId Correct\n")
                        else:
                            logger.error("V3 DataId NotCorrect\n")

                else:
                    logger.error(tmp_file.replace(root, "") + " is not exits")


# 从得到的结果集中找到所有的DataId,用来查看比较文件中的DataId
def get_all_dataId(set_r, data_id_index):
    set_d = set()
    for r in set_r:
        if r:  # 去除set中的空值
            set_d.add(r.split("|")[data_id_index])
    return set_d


# 读取压缩文件，返回压缩文件内的文件
def read_Zip(file):
    zfile = zipfile.ZipFile(file, 'r')
    data = set()
    for filename in zfile.namelist():
        data = set(zfile.read(filename).split("\r\n"))
    return data


root = "D:\QA\GEDF\GeDataFeed-MOCAL4724\GEDF"
file_exists(root)