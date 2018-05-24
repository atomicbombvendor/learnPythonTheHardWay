# coding=utf-8
# 读取所有的国家列表，然后用配置文件组装
import codecs


# 从配置文件中读取所有需要用来填充msg文件的数据；列表封装
def Get_Value():
    file_object = open(value_file, 'r')  # r,只读 w:写之前会清空文件的内容 a:追加的方式，在原本内容中继续写
    for line in file_object:
        line = line.strip('\n')  # 去掉换行符
        values.append(line)


def Generate_file(source, target):
    with codecs.open(target, 'w', 'utf-8') as t_f: # 清空文件
        t_f.write(r'''<?xml version="1.0" encoding="utf-8"?>
<MessageSet>
    <ReferenceId>636119897950570000ZdVfqnNQ1T2magoD5uzH5A</ReferenceId>
    <NumberofResults>2000</NumberofResults>
''')

    Get_Value()  # 返回一个文件中的列表
    count = 0
    for val in values:
        tmp_val = val
        count = count + 1
        content = Read_Replace_holder(source, tmp_val, count)
        write_file(target, content)

    with codecs.open(target, 'a', 'utf-8') as t_f:# 清空文件
        t_f.write("</MessageSet>")

    print "生成Message文件完成"


# 从文件中读取所有的CompanyId（或者ShareClassId),然后去处重复的。
# 截取每一行的前10个字符，装入list，然后去重
def distinct_companyId(source, target):
    ids = []
    source_file = codecs.open(source, 'r', 'utf-8')
    for line in source_file:
        data = line.strip()  # 去除空行
        if len(data) != 0:
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
# tmp_val 从文件中读取的值，current_index 当前是文件中的第几行
def Read_Replace_holder(source, tmp_val, current_index):
    place_holder_C = '@place_holder_country@'
    place_holder_N = '@num@'
    place_holder_S = '@shareClassId@'
    content = ''
    with open(source, 'r') as f:
        lines = f.readlines()
    for line in lines:
        tmp = line
        if place_holder_C in line:
            tmp = tmp.replace(place_holder_C, tmp_val)
        if place_holder_N in line:
            tmp = tmp.replace(place_holder_N, str(current_index))
        if place_holder_S in line:
            tmp = tmp.replace(place_holder_S, tmp_val)
        content = content + tmp
    return content


def write_file(target, data):
    f = codecs.open(target, 'a', 'utf-8')  # w会清空原来的内容 a为追加
    f.write(str(data) + '\r\n')  # \r\n为换行符
    f.close()


# 使用Value_file文件内的CompanyId列表生成Msg的文件
value_file = "ValueFile.txt"  # 这是配置文件用来填充占位符的
values = []
# distinct_companyId('CompanyId.txt', 'new_companyId.txt')
# 读取msg.txt msg_shareClassId.txt new_companyId.txt文件的内容，生成GEDF msg文件
# Generate_file(source_Monthly, config_Monthly)
Generate_file('msgtempalte.txt', 'msg_companyId.txt')
# Generate_file(source_DeadwoodMonthly, config_DeadwoodMonthly)
