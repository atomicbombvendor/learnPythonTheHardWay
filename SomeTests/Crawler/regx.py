# coding=utf-8
# http://cuiqingcai.com/977.html
import re

pattern = re.compile(r"\S")
#  使用re.match匹配文本，获得匹配结果，无法匹配时将返回None
result1 = re.match(pattern, 'hello')
result2 = re.match(pattern, 'helloo CQC!')
result3 = re.match(pattern, 'helo CQC!')
result4 = re.match(pattern, 'hello CQC! hello hello hello hello')

# 如果1匹配成功
if result1:
    # 使用Match获得分组信息
    print result1.group()
else:
    print '1匹配失败！'

# 如果2匹配成功
if result2:
    # 使用Match获得分组信息
    print result2.group()
else:
    print '2匹配失败！'

# 如果3匹配成功
if result3:
    # 使用Match获得分组信息
    print result3.group()
else:
    print '3匹配失败！'

# 如果4匹配成功
if result4:
    # 使用Match获得分组信息
    print result4.group()
else:
    print '4匹配失败！'


m = re.match(r'(\w+) (\w+)(?P<sign>.{3})', 'adf helloWar worldWant!+! helldoWdar worlddWandt!+!')

print "m.string:", m.string
print "m.re:", m.re
print "m.pos:", m.pos
print "m.endpos:", m.endpos
print "m.lastindex:", m.lastindex
print "m.lastgroup:", m.lastgroup
print "m.group():", m.group()  # group返回括号匹配上的内容
print "m.group(1,2):", m.group(1, 2)
print "m.groups():", m.groups()
print "m.groupdict():", m.groupdict()
print "m.start(2):", m.start(2)
print "m.end(2):", m.end(2)
print "m.span(2):", m.span(2)
print r"m.expand(r'\g \g\g'):", m.expand(r'\2 \1\3')

pattern = re.compile(r'(\w+)')
match = re.search(pattern, 'hellow world !!@##@')
if match:
    print match.group()
    print match.string

# 搜索string，以列表形式返回全部能匹配的子串。我们通过这个例子来感受一下
print re.findall(pattern, 'hellow world !!@##@')

# 按照能够匹配的子串将string分割后返回列表。maxsplit用于指定最大分割次数，不指定将全部分割。我们通过下面的例子感受一下。
pattern = re.compile(r'\d+')
print re.split(pattern, 'one1two2three3four4')

for item in re.finditer(pattern, 'one1two2three3'):
    print item.group(),

# re.sub(pattern, repl, string[, count])
# 使用repl替换string中每一个匹配的子串后返回替换后的字符串。
# 当repl是一个字符串时，可以使用\id或\g、\g引用分组，但不能使用编号0。
# 当repl是一个方法时，这个方法应当只接受一个参数（Match对象），并返回一个字符串用于替换（返回的字符串中不能再引用分组）。
# count用于指定最多替换次数，不指定时全部替换。
pattern = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'

print re.sub(pattern, r'\2 \1', s)


def func(m):
    return m.group(1).title() + ' ' + m.group(2).title()
# title 会首字母大写内容

print re.sub(pattern, func, s)

# re.subn(pattern, repl, string[, count])
# 返回 (sub(repl, string[, count]), 替换次数)。
pattern = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'

print re.subn(pattern, r'\2 \1', s)


def func(m):
    return m.group(1).title() + ' ' + m.group(2).title()


print re.subn(pattern, func, s)
