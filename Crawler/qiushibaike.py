# coding=utf-8
import urllib
import urllib2
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

page = 1
url = "http://www.qiushibaike.com/hot/page/" + str(page)
user_agent = 'Mozilla/4.2 (compatible; MSIE 5.5; Windows NT)'
header = {'User-Agent': user_agent}

try:
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)
    # print response.read()

    content = response.read().decode('utf-8')
    pattern = re.compile('<h2>\n(.*?)</h2>.*?content".*?span>\n(.*?)</span>.*?<!--.*?-->(.*?)number">(.*?)</i>', re.S)
                                                                                #   img           comment
    # pattern = re.compile(
    #     '<h2>(.*?)</h2.*?class="content".*?span>(.*?)' +
    #     # h2<用户名>/h2任意字符class="content""任意字符span>(内容)
    #     '</.*?!--.*?-->(.*?)</.*?number">(.*?)</i>', re.S)
    #     # </任意字符!--尽可能少的任意字符-->(这段内容包含了一段字符串)</任意字符number">(评论数)</i>
    items = re.findall(pattern, content)
    for item in items:
        havImg = re.search("img", item[2])
        if havImg is not None:
            imgPattern = re.compile('<img.*?src="(.*?)" alt.*?>', re.S)
            imgURL = re.findall(imgPattern, item[2])
            print "用户名: %s内容: %s\n图片链接: %s\n评论数: %s\n" % (item[0], item[1].replace("\n", ""), imgURL[0], item[3])
        else:
            print "用户名: %s内容: %s\n评论数: %s\n" % (item[0], item[1].replace("\n", ""), item[3])

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
