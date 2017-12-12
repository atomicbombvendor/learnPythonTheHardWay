# coding=utf-8
import urllib2
import re


class Tool:
    # 去除img标签，7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 去除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签删除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        # def sub(pattern, repl, string, count=0, flags=0):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n  ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


class TieBa:
    # 初始化，传入地址，以及是否只看楼主的参数,floorTag:为1就是往文件中写入楼层分隔符
    def __init__(self, url, seelZ, floorTag):
        self.url = url
        self.seelZ = "?see_lz="+str(seelZ)
        self.tool = Tool()
        self.file = None
        # 默认标题，如果没有获取到网页上帖子的标题，此将作为文件的名字
        self.defaultTitle = "百度贴吧"
        self.floorTag = floorTag
        # 楼层序号
        self.floor = 1

        self.enable = False
        self.user_agent = 'Mozilla/4.2 (compatible; MSIE 5.5; Windows NT)'
        self.header = {'User-Agent': self.user_agent}

    # http: // blog.csdn.net / u010412719 / article / details / 50199047
    # def getPageCount(self, pageNum):
