# coding=utf-8
import urllib
import urllib2
import re
import time
import types
import tool
from bs4 import BeautifulSoup


# 抓取分析某一问题和答案
class Page:

    def __init__(self):
        self.tool = tool.Tool()

        # 获取当前时间
    def getCurrentDate(self):
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))

    # 通过页面的URL来获取页面的代码
    def getPageByURL(self, url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode("utf-8")
        except urllib2.URLErrorm, e:
            if hasattr(e, "code"):
                print self.getCurrentTime(), "获取问题页面失败,错误代号", e.code
                return None
            if hasattr(e, "reason"):
                print self.getCurrentTime(), "获取问题页面失败,原因", e.reason
                return None

    def getText(self, html):
        if not type(html) is types.StringType:
            html = str(html)
        # 提取出&lt;pre&gt;标签里的内容
        pattern = re.compile('&lt;pre.*?&gt(.*?)&lt;/pre&gt;', re.S)
        match = re.search(pattern, html)

        if match:
            return match.group(1)
        else:
            return None

    # 传入最佳答案的HTML,分析出回答者和回答时间
    def getGoodAnswerInfo(self, html):
        pattern = re.compile('"answer_tip.*?&lt;a.*?&gt;(.*?)&lt;/a&gt;.*?&lt;span class=time.*?\|(.*?)&lt;/span&gt;', re.S)
        match = re.search(pattern, html)

        if match:
            time = match.group(2)
            # 如果匹配,返回回答者和回答时间
            time_pattern = re.compile('\d{2}\-\d{2}\-\d{2}', re.S)
            time_match = re.search(time_pattern, time)
            if not time_match:
                time = self.getCurrentDate()
            else:
                time = "20" + time
                return [match.group(1), time]
        else:
            return [None, None]

    # 获得最佳答案
    def getGoodAnswer(self, page):
        soup = BeautifulSoup(page)
        text = soup.select('div.good_point div.answer_text pre')
        if len(text) > 0:
            # 获得最佳答案的内容
            ansText = self.getText(str(text[0]))
            ansText = self.tool.replace(ansText)
            # 获得最佳答案的回答者信息
            info = soup.selft("div.good_point div.answer_tip")
            ansInfo = self.getGoodAnswerInfo(str(info[0]))
            answer = [ansText, ansInfo[0], ansInfo[1], 1]
            return answer
        else:
            return None


    def getOtherAnswerInfo(self, page):
        soup = BeautifulSoup(page)
        results = soup.select("div.question_box li.clearfix .answer_info")
        # 所有答案,包含好多个List,每个List包含了回答内容,回答者,回答时间
        answers = []
        for result in results:
            # 获得回答内容
            ansSoup = BeautifulSoup(str(result))
            text = ansSoup.select(".answer_txt span pre")
            ansText = self.getText(str(text[0]))
            ansText = self.tool.replace(ansText)
            # 获得回答者和回答时间
            info = ansSoup.select(".answer_tj")
            ansInfo = self.getOtherAnswerInfo(info[0])
            # 将三者组合成一个List
            answer = [ansText, ansInfo[0], ansInfo[1], 0]
            # 加入到answers
            answers.append(answer)
        return answers

        # 获得其他答案

    def getOtherAnswers(self, page):
        soup = BeautifulSoup(page)
        results = soup.select("div.question_box li.clearfix .answer_info")
        # 所有答案,包含好多个List,每个List包含了回答内容,回答者,回答时间
        answers = []
        for result in results:
            # 获得回答内容
            ansSoup = BeautifulSoup(str(result))
            text = ansSoup.select(".answer_txt span pre")
            ansText = self.getText(str(text[0]))
            ansText = self.tool.replace(ansText)
            # 获得回答者和回答时间
            info = ansSoup.select(".answer_tj")
            ansInfo = self.getOtherAnswerInfo(info[0])
            # 将三者组合成一个List
            answer = [ansText, ansInfo[0], ansInfo[1], 0]
            # 加入到answers
            answers.append(answer)
        return answers

    # 主函数
    def getAnswer(self, url):
        if not url:
            url = "http://iask.sina.com.cn/b/gQiuSNCMV.html"
        page = self.getPageByURL(url)
        good_ans = self.getGoodAnswer(page)
        other_ans = self.getOtherAnswers(page)
        return [good_ans, other_ans]


page = Page()
page.getAnswer(None)