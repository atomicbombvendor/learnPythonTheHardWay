# coding=utf-8
import codecs
import re
import zipfile

# 把路径下的所有Id读取出来,并出重
# 构造一个List,遍历List中的文件
import os


def start_read_id(root, files):
        companyId_in_zip = []
        for file in files:
            full_file_path = os.path.join(root, file)
            print("Process " + full_file_path + "\n")
            companyId_in_zip.extend(read_id_from_zip(full_file_path))  # 得到压缩包下的所有Id

        func = lambda x, y: x if y in x else x + [y]
        companyId_in_zip = reduce(func, [[], ] + companyId_in_zip)  # 去重
        return companyId_in_zip

def write_file(target, data):
    f = codecs.open(target, 'w', 'utf-8')  # w会清空原来的内容 a为追加
    f.write(str(data) + '\r\n')  # \r\n为换行符
    f.close()


# 从Zip文件解析出所有的CompanyId
def read_id_from_zip(file):
    zfile = zipfile.ZipFile(file, 'r')
    pattern = r"(0C[0-9A-Za-z]{8}|0P[0-9A-Za-z]{8})"
    data = []
    for filename in zfile.namelist():
        match = re.search(pattern, filename)
        if match:
            data.append(match.group())
    return data

root = 'z:\\'
files = [
    '\AFR\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip',
    '\ANZ\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip',
    '\ASP\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip',
    '\EUR\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip',
    '\IPM\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip',
    '\LTA\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip',
    '\NRA\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip',
    '\UKI\Fundamental\FinancialStatements\Delta\Delta_FinancialStatementsAOR_2018-04-02.zip'
]

ids = start_read_id(root, files)
write_file("generate_all_id.dat", ids)
