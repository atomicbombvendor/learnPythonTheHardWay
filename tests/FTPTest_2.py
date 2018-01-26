
# coding=utf-8
import codecs
import re
from ftplib import FTP

# ftp://ftp.morningstar.com/equity2/monthly/Country
# ftp://ftp.morningstar.com/equity2/DeadwoodMonthly/Country
# ftp://ftp.morningstar.com/equity2/DailyDelta/Country

loc = locals()

ftp = FTP()
# ftp.set_debuglevel(2)
ftp.connect(host='ftp.morningstar.com')
ftp.login('OnDemandMaster', 'OnDemandMasterNew1234')

monthly = "/Equity2/Monthly/"
deadwoodMonthly = "/Equity2/DeadwoodMonthly/"
dailyDelta = "/Equity2/DailyDelta/"

folder_sum = 0
file_sum = 0
total_file_size = 0

files = []


def search_file(start_dir):
    ftp.cwd(start_dir)
    print "current path >> ", ftp.pwd()
    dir_res = []
    ftp.dir('.', dir_res.append)  # 对当前目录进行dir(), 将结果放入列表 # ftp.dir() #显示目录下的文件信息
    for i in dir_res:
        if not i.startswith("d"):  # drwxrwxrwx startWith是D 表示的是目录
            global file_sum, total_file_size
            file_sum += 1
            val = i.split(" ")[-1]
            total_file_size += ftp.size(val)
            if ftp.pwd().endswith('/'):
                tmp = process_file_name(ftp.pwd() + val)
                if tmp:
                    add_files(tmp)
                    print tmp + "     " + str(ftp.size(val)) + " B"  # 打印出每个文件路径和大小
                pass
            else:
                tmp = process_file_name(ftp.pwd() + "/" + val)
                if tmp:
                    add_files(tmp)
                    print tmp + "     " + str(ftp.size(val)) + " B"
                pass
        else:  # 是目录的情况
            if not (i.split(" ")[-1] == '.' or i.split(" ")[-1] == '..'):
                global folder_sum
                folder_sum += 1
                search_file(ftp.pwd() + "/" + i.split(" ")[-1])
                ftp.cwd('..')


def process_file_name(file_name):
    if 'StatutoryTaxRate' not in file_name:
        pattern = r'(/.*/.*)(\d{6})(\.(zip|ctrl|txt))'
        match_obj = re.match(pattern, file_name, re.S)
        if match_obj:
            return match_obj.group(1)


def add_files(file_name):
    if file_name not in files:
        files.append(file_name)


def sum_file(file_path):
    search_file(file_path)
    print "folder number is " + str(folder_sum) + ", file number is " + str(file_sum) + ", Total size is " \
          + str(total_file_size) + " B"
    print "files length >>", len(files)
    write_file(file_path, files)


def write_file(file_name, data):
    f = codecs.open(get_variable_name(file_name)+'.txt', 'w', 'utf-8')
    for i in data:
        f.write(str(i) + '\r\n')  # \r\n为换行符
    f.close()


def get_variable_name(variable):  # 得到变量的名字
    print loc
    for key in loc:
        if loc[key] == variable:
            return key


if __name__ == '__main__':
    # sum_file(monthly)
    # sum_file(deadwoodMonthly)
    sum_file(dailyDelta)
