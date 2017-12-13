# coding=utf-8
import urllib2
import re


class Tool:
    def __init__(self):
        # 去除img标签，7位长空格
        self.removeImg = re.compile('<img.*?>| {7}|')
        # 去除超链接标签
        self.removeAddr = re.compile('<a.*?>|</a>')
        # 把换行的标签换为\n
        self.replaceLine = re.compile('<tr>|<div>|</div>|</p>')
        # 将表格制表<td>替换为\t
        self.replaceTD = re.compile('<td>')
        # 把段落开头换为\n加空两格
        self.replacePara = re.compile('<p.*?>')
        # 将换行符或双换行符替换为\n
        self.replaceBR = re.compile('<br><br>|<br>')
        # 将其余标签删除
        self.removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        # def sub(pattern, repl, string, count=0, flags=0):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n  ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格）。
        return x.strip()


class TieBa:
    # 初始化，传入地址，以及是否只看楼主的参数,floorTag:为1就是往文件中写入楼层分隔符
    def __init__(self, url_p, see_lz, floor_tag):
        self.url = url_p
        self.see_lz = "?see_lz=" + str(see_lz)
        self.tool = Tool()
        self.file = None
        # 默认标题，如果没有获取到网页上帖子的标题，此将作为文件的名字
        self.defaultTitle = "百度贴吧"
        self.floorTag = floor_tag
        # 楼层序号
        self.floor = 1

        self.enable = False
        self.user_agent = 'Mozilla/4.2 (compatible; MSIE 5.5; Windows NT)'
        self.header = {'User-Agent': self.user_agent}

    # http: // blog.csdn.net/u010412719/article/details/50199047
    # 根据传入的页码来获取帖子的内容
    def getPageCount(self, page_num):
        fullUrl = self.url + self.see_lz + "&pn=" + str(page_num)
        try:
            request = urllib2.Request(fullUrl, headers=self.header)
            response = urllib2.urlopen(request)
            content = response.read().decode("utf-8")
            print content
            return content
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason

    # 得到帖子的标题
    def getPageTile(self, page_num):
        content = self.getPageCount(page_num)
        pattern = re.compile(r'<h3 class="core_title_txt pull-left text-overflow .*?>(.*?)</h3>', re.S)
        title = re.search(pattern, content)

        if title:
            print title.group(1).strip()
            return title.group(1).strip()
        else:
            print None

        # 得到帖子的作者
    def getPageAuthor(self, page_num):
        content = self.getPageContent(page_num)
        # <div class="louzhubiaoshi  j_louzhubiaoshi" author="懂球君">
        pattern = re.compile(r'<div class="louzhubiaoshi  j_louzhubiaoshi" author="(.*?)">', re.S)
        author = re.search(pattern, content)
        if author:
            print author.group(1).strip()  # 测试输出
            return author.group(1).strip()
        else:
            print None

        # 得到帖子的总页数和总回复数
    def getPageTotalPageNum(self, page_num):
        content = self.getPageContent(page_num)
        # <li class="l_reply_num" style="margin-left:8px" ><span class="red"
        # style="margin-right:3px">1</span>回复贴，共<span class="red">1</span>页</li>
        pattern = re.compile(
            r'<li class="l_reply_num".*? style="margin-right:3px">(.*?)</span>.*?<span class="red">(.*?)</span>', re.S)
        totalPageNum = re.search(pattern, content)
        if totalPageNum:
            print totalPageNum.group(1).strip(), totalPageNum.group(2).strip()  # 测试输出
            # print totalPageNum[0],totalPageNum[1]
            return totalPageNum.group(1).strip(), totalPageNum.group(2).strip()  # 第一个返回值为回复个数，第二个返回值为帖子的页数
        else:
            print "没找到"
            print None

    # 得到帖子的总页数和总回复数
    def getPageTotalPageNum(self, page_num):
        content = self.getPageCount(page_num)
        pattern = re.compile(
            r'<li class="l_reply_num".*? style="margin-right:3px">(.*?)</span>.*?<span class="red">(.*?)</span>', re.S)
        totalPageNum = re.search(pattern, content)
        if totalPageNum:
            print totalPageNum.group(1).strip(),totalPageNum.group(2).strip()
            return totalPageNum.group(1).strip(), totalPageNum.group(2).strip()  # 第一个返回值为回复个数，第二个返回值为帖子的页数
        else:
            print "没找到"
            return None

    # 提取贴子内容
    def getContent(self, page_num):
        content = self.getPageCount(page_num)
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, content)
        floor = 1
        contents = []
        for item in items:
            # 将每个楼层的内容进行去除标签处理，同时在前后加上换行符
            tempContent = "\n" + self.tool.replace(item) + "\n"
            contents.append(tempContent.encode("utf-8"))
            # 测试输出
            print floor, u"楼-------------------------------------------\n"
            print self.tool.replace(item)
            floor += 1
        return contents

    # 将内容写入文件中保存
    def writedata2File(self, contents):
        for item in contents:
            if self.floorTag == "1":
                floorLine = u"\n"+str(self.floor)+u"-------------------\n"
                self.file.write(floorLine)
                print u"正在向文件中写入第"+str(self.floor)+u"楼的内容"
                self.file.write(item)
                self.floor += 1

    # 根据获取网页贴子的标题来在目录下建立一个同名的.txt文件
    def newFileAccTitle(self, title):
        if title is not None:
            self.file = open(title+".txt", "w+")
        else:
            self.file = open(self.defaultTitle+".txt", "w+")

    # 抓取贴吧的启动程序
    def start(self, page_num):
        content = self.getPageCount(page_num)

        title = self.getPageTile(page_num)

        self.newFileAccTitle(title)

        author = self.getPageAuthor(page_num)

        contents = self.getContent(page_num)

        try:
            self.writedata2File(contents)
        except IOError, e:
            print "写入文件异常, 原因"+e.message
        finally:
            print "写入文件完成"


# 测试代码
url = "http://www.tieba.baidu.com/p/4197307435"
seeLZ = input("input if see louzhu: ")
pageNum = input("input page Num: ")
floorTag = input("input floorTag: ")
baidutieba = TieBa(url, seeLZ, floorTag)
baidutieba.start()

# content=baidutieba.getPageContent(pageNum)#调用函数
# 开始解析得到帖子标题
# baidutieba.getPageTitle(1)
# 开始解析得到帖子的作者
# baidutieba.getPageAuthor(1)
# baidutieba.getPageTotalPageNum(1)
# 解析帖子中的内容
# baidutieba.getContent(pageNum)
