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
import codecs
import logging
import os
import string
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
                            # region 从压缩文件中提取1007的数据到目录下; 适用于 v3 SecurityReference
                            data_set_1007 = extract_id(read_Zip(tmp_file), data_id_index=2, data_id="1007")

                            if "Daily" in tmp_file:
                                schedule = "Daily"
                            else:
                                schedule = "Monthly"

                            save_extract_data_for_SecurityReference(data_set_1007, region, schedule)
                            # endregion

                            # region 从压缩文件中提取1007的数据，并且该条记录包含ISIN前缀; 用于 v3 SecurityReference
                            data_set_1007 = extract_id_prefix(read_Zip(tmp_file), data_id_index=2, data_id="1007")

                            if "Daily" in tmp_file:
                                schedule = "Daily"
                            else:
                                schedule = "Monthly"

                            save_extract_data_for_SecurityReference(data_set_1007, "NM_"+region, schedule)
                            # endregion

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


# 把提取的固定Id的记录存储起来; set的大小为空 则不输出
def save_extract_data_for_SecurityReference(data_set, region, schedule):
    if len(data_set) == 0:
        return
    root = "D:\QA\GEDF\GeDataFeed-R180517\Result\SpecialResult\\"
    if "Deadwood" in region:
        region = region.replace("\\", "_")
    folder = "%s_%s_%s_%s\%s" % ("v3", region, schedule, "SecurityReference", "1007.dat")
    file_path = root + folder
    write_file(file_path, data_set)


# 提取固定Id的整条记录
def extract_id(set_r, data_id_index, data_id):
    set_d = set()
    for r in set_r:
        if r:  # 去除set中的空值
            di = r.split("|")[data_id_index]
            if data_id in di:
                set_d.add(r)
    return set_d

# 提取固定Id，并且包含某些前缀的整条记录
def extract_id_prefix(set_r, data_id_index, data_id):
    prefixs = {
        "AS", "AI", "AG", "AW", "BS", "BZ", "BM", "BQ", "CA", "KY", "CW", "DM", "GD", "GU", "GY", "HT", "MH", "YT",
    "FM", "MP", "PW", "PH", "PR", "BL", "KN", "LC", "MF", "VC", "SX", "GS", "SR", "TT", "US", "UM", "VG", "VI"
    }
    set_d = set()
    for r in set_r:
        if r:  # 去除set中的空值
            dataId = r.split("|")[data_id_index]
            data_prefix = r.split("|")[data_id_index+1][0:2]
            if (data_id in dataId) and (data_prefix in prefixs):
                set_d.add(r)
    return set_d

# 写数据到文件;file_path是文件的路径+文件名
def write_file(file_path, data_set):
    if not os.path.exists(os.path.split(file_path)[0]):
        os.makedirs(os.path.split(file_path)[0])  # 创建级联目录
    with codecs.open(file_path, 'w', 'utf-8') as fnl:
        for line in list(data_set):
            fnl.write(str(line) + "\r\n")


# 读取压缩文件，返回压缩文件内的文件
def read_Zip(file):
    zfile = zipfile.ZipFile(file, 'r')
    data = set()
    for filename in zfile.namelist():
        data = set(zfile.read(filename).split("\r\n"))
    return data


# root = "D:\QA\GEDF\GeDataFeed-MOCAL4724\GEDF"
# file_exists(root)

root = "D:\QA\GEDF\GeDataFeed-R180517\GEDF"
file_exists(root)