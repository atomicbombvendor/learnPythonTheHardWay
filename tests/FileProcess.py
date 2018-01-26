# coding=utf-8
import codecs

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


process_file(dailyDelta, dailyDelta2)