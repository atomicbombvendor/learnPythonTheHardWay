# coding=utf-8
import codecs

import os

monthly = "monthly.txt"
monthly2 = "monthly2.txt"
deadwood = "deadwoodMonthly.txt"
deadwood2 = "deadwoodMonthly2.txt"
dailyDelta = "dailyDelta.txt"
dailyDelta2 = "dailyDelta2.txt"


def process_file(source, target):
    result = []
    try:
        file_object = open(source, 'r')  # r,只读 w:写之前会清空文件的内容 a:追加的方式，在原本内容中继续写
        for line in file_object:
            line = line.strip('\n') # 去掉换行符
            val_zip = line + 'yyyyMMdd.zip'
            val_ctrl = line + 'yyyyMMdd.ctrl'
            add_vals(result, val_zip)
            add_vals(result, val_ctrl)
        write_file(target, result)
        print "Done"
    except IOError:
        print "找不到这个文件".decode('utf8').encode('gbk')


def write_file(target, data):
    f = codecs.open(target, 'w', 'utf-8')  # w会清空原来的内容 a为追加
    for i in data:
        f.write(str(i) + '\r\n')  # \r\n为换行符
    f.close()


def add_vals(result, val):
    if val not in result:
        result.append(val)


# 将文件中的<file size的行都注释掉，不包括 marketCap
def add_comment(file):
    file_data = ""
    file_object = codecs.open(file, 'r')
    for line in file_object:
        if '<filename filesize="20b">' in line:
            if 'MarketCap_' not in line:
                line = line.strip('\r\n').strip('\t')
                line = '\t\t<!--' + line + ' -->\r\n'
        file_data += line
    return file_data


def clear_blank_lin(file_path):
    if ('.bat' not in file_path) or('DevT' in file_path) or ('ProdT' in file_path):
        return
    file_object = codecs.open(file_path, 'r')
    target = ''
    if 'Dev' in file_path:
        target = file_path.replace('Dev', 'DevT')
    elif 'Production' in file_path:
        target = file_path.replace('Production', 'ProdT')
    a = []
    target_file = codecs.open(target, 'w', 'utf-8')

    try:
        for line in file_object:
            if '\r' in line or '\n' in line:
                line = line.strip('\r').strip('\n')
            target_file.write(line)
    finally:
        file_object.close()
        target_file.close()


def get_all_file(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if '.bat' in os.path.split(f)[1]:
                L.append(os.path.join(root, f))
    return L


def get_all_file_2(file_dir, list_name):  # 传入存储的list
    for f in os.listdir(file_dir):
        file_path = os.path.join(file_dir, f)
        if os.path.isdir(file_path):
            get_all_file_2(file_path, list_name)
        else:
            list_name.append(file_path)
    return list_name


def process_company_file():
    file_object = codecs.open('CompanyId.txt', 'r')
    r1 = []
    for line in file_object:
        r1 += line[11:16].split(" ")

    # 去重 没有work
    func = lambda x, y: x if y in x else x + [y]
    reduce(func, [[], ] + r1)

    f = codecs.open('CompanyId.txt', 'w', 'utf-8')  # w会清空原来的内容 a为追加
    for i in set(r1):
        f.write(str(i.strip('\n')) + ',')  # \r\n为换行符
    f.close()


process_company_file()

# result = []
# get_all_file_2('D:\Work\SourceTree\GEDF\ge-gedf-old\EquityDataFeed\JobCommands', result)
# for r in result:
#     clear_blank_lin(r)
# process_file(dailyDelta, dailyDelta2)
# add_comment('config_DailyDelta.xml')


