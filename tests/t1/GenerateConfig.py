# coding=utf-8
# 读取所有的国家列表，然后用配置文件组装
import codecs

country = "new_companyId.txt"  # 这是配置文件用来填充占位符的
countrys = []

config_DailyDelta = "config_DailyDelta.xml"
config_DeadwoodMonthly = "config_DeadwoodMonthly.xml"
config_Monthly = "config_Monthly.xml"

source_DailyDelta = 'file_DailyDelta.txt'
source_DeadwoodMonthly = 'file_DeadwoodMonthly.txt'
source_Monthly = 'file_Monthly.txt'

val_DailyDelta = ''
val_DeadwoodMonthly = ''
val_Monthly = ''


def Get_Country():
    file_object = open(country, 'r')  # r,只读 w:写之前会清空文件的内容 a:追加的方式，在原本内容中继续写
    for line in file_object:
        line = line.strip('\n')  # 去掉换行符
        countrys.append(line)


def Generate_file(source, target):
    codecs.open(target, 'w', 'utf-8').write('<data>\r\n')  # 清空文件
    Get_Country()
    count = 0
    for i in countrys:
        tmp_c = i
        count = count + 1
        content = Read_Replace_holder(source, tmp_c, count)
        write_file(target, content)
    codecs.open(target, 'a', 'utf-8').write('</data>\r\n')  # 清空文件
    print "生成Message文件完成"


# 从文件中读取所有的CompanyId（或者ShareClassId),然后去处重复的。
# 截取每一行的前10个字符，装入list，然后去重
def distinct_companyId(source, target):
    ids = []
    source_file = codecs.open(source, 'r', 'utf-8')
    for line in source_file:
        ids.append(line[0:10])
    tmp = list(set(ids))
    data = ''
    for val in tmp:
        data += val + "\r\n"
    write_file(target, data)


# 定义一个函数，带有4个参数
# x 表示要更新的文件名称
# y 表示要被替换的内容
# z 表示 替换后的内容
# s 默认参数为 1 表示只替换第一个匹配到的字符串
# 如果参数为 s = 'g' 则表示全文替换
def Read_Replace_holder(source, c, num):
    place_holder_C = '@place_holder_country@'
    place_holder_N = '@num@'
    place_holder_S = '@shareClassId@'
    content = ''
    with open(source, 'r') as f:
        lines = f.readlines()
    for line in lines:
        tmp = line
        if place_holder_C in line:
            tmp = tmp.replace(place_holder_C, c)
        if place_holder_N in line:
            tmp = tmp.replace(place_holder_N, str(num))
        if place_holder_S in line:
            tmp = tmp.replace(place_holder_S, c)
        content = content + tmp
    return content


def write_file(target, data):
    f = codecs.open(target, 'a', 'utf-8')  # w会清空原来的内容 a为追加
    f.write(str(data) + '\r\n')  # \r\n为换行符
    f.close()


# distinct_companyId('CompanyId.txt', 'new_companyId.txt')

# Generate_file(source_Monthly, config_Monthly)
Generate_file('msg.txt', 'msg_shareClassId.txt')
# Generate_file(source_DeadwoodMonthly, config_DeadwoodMonthly)
