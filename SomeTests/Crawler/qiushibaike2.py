# coding=utf-8
import re
import urllib2


class QSBK:
    def __init__(self):
        self.enable = False
        self.page = 1
        self.user_agent = 'Mozilla/4.2 (compatible; MSIE 5.5; Windows NT)'
        self.header = {'User-Agent': self.user_agent}
        self.catch_url = 'http://www.qiushibaike.com/hot/page/'
        self.pattern = re.compile('<h2>\n(.*?)</h2>.*?content".*?span>\n(.*?)</span>.*?<!--.*?-->(.*?)number">(.*?)</i>', re.S)

    def get_content_with_page(self, page):
        try:
            request = urllib2.Request(self.catch_url+str(page), headers=self.header)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "attr"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return ""

    def get_stories_from_content(self, content):
        return re.findall(self.pattern, content)

    def start(self):
        self.enable = True

        while self.enable:
            content = self.get_content_with_page(self.page)
            stories = self.get_stories_from_content(content)

            if len(stories) > 0:
                for item in stories:
                    hasimg = re.search("img", item[2])
                    if hasimg is not None:
                        imgpattern = re.compile('<img.*?src="(.*?)" alt.*?>', re.S)
                        imgurl = re.findall(imgpattern, item[2])
                        print "用户名: %s内容: %s\n图片链接: %s\n评论数: %s\n" % (
                            item[0], item[1].replace("\n", ""), imgurl[0], item[3])
                    else:
                        print "用户名: %s内容: %s\n评论数: %s\n" % (item[0], item[1].replace("\n", ""), item[3])

                    print "按Enter继续..."
                    raw_input()

            self.page += 1


spider = QSBK()
spider.start()