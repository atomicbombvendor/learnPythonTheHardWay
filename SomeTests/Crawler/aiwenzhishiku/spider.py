# coding=utf-8
import urllib2
import re
import time
import types

from BeautifulSoup import BeautifulSoup

import page
import mysql
import sys

class Spider:

    def __init__(self):
        self.page_num = 1
        self.total_num = None
        self.page_spider = page.Page()
        self.mysql = mysql.Mysql()

        # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

        # 获取当前时间
    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def getPageURLByNum(self, page_num):
        page_url = "http://iask.sina.com.cn/c/978-all-" + str(page_num) + "-new.html"
        return page_url

    def getPageByNum(self, page_num):
        request = urllib2.Request(self.getPageURLByNum(page_num))
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print self.getCurrentTime(), "获取页面失败,错误代号", e.code
                return None
            if hasattr(e, "reason"):
                print self.getCurrentTime(), "获取页面失败,原因", e.reason
                return None
            else:
                return response.read().decode("utf-8")

    def getTotalPageNum(self):
        print self.getCurrentTime(), "正在获取目录页面个数，请稍等"
        page_t = self.getPageByNum(1)
        # 匹配所有的页码数,\u4e0b\u4e00\u9875是下一页的UTF8编码
        pattern = re.compile(
            u'&lt;span class="more".*?&gt;.*?&lt;span.*?&lt;a href.*?class=""&gt;(.*?)&lt;/a&gt;\s*&lt;a.*?\u4e0b\u4e00\u9875&lt;/a&gt;',
            re.S)
        match = re.search(pattern, page_t)
        if match:
            return match.group(1)
        else:
            print self.getCurrentTime(), "获取总页码失败"

    def getTotalPageNum2(self):
        print self.getCurrentTime(), "正在获取目录页面个数，请稍等"
        page_t = self.getPageByNum(1)
        # 匹配所有的页码数,\u4e0b\u4e00\u9875是下一页的UTF8编码
        pattern = re.compile(
            u'&lt;span class="more".*?&gt;.*?&lt;span.*?&lt;a href.*?class=""&gt;(.*?)&lt;/a&gt;\s*&lt;a.*?\u4e0b\u4e00\u9875&lt;/a&gt;',
            re.S)
        match = re.search(pattern, page_t)
        if match:
            return match.group(1)
        else:
            print self.getCurrentTime(), "获取总页码失败"


    def getQuestionInfo(self, question):
        if not type(question) is types.StringType:
            question = str(question)
        pattern = re.compile(
            u'&lt;span.*?question-face.*?&gt;.*?&lt;img.*?alt="(.*?)".*?&lt;/span&gt;.*?&lt;a href="(.*?)".*?&gt;(.*?)&lt;/a&gt;.*?answer_num.*?&gt;(\d*).*?&lt;/span&gt;.*?answer_time.*?&gt;(.*?)&lt;/span&gt;',
            re.S)
        match = re.search(pattern, question)
        if match:
            # 获得提问者
            author = match.group(1)
            # 问题链接
            href = match.group(2)
            # 问题详情
            text = match.group(3)
            # 回答个数
            ans_num = match.group(4)
            # 回答时间
            time = match.group(5)
            time_pattern = re.compile('\d{4}\-\d{2}\-\d{2}', re.S)
            time_match = re.search(time_pattern, time)
            if not time_match:
                time = self.getCurrentDate()
            return [author, href, text, ans_num, time]
        else:
            return None

    def getQuestions(self, page_num):
        page = self.getPageByNum(page_num)
        soup = BeautifulSoup(page)

        questions = soup.select("div.question_list ul li")
        for question in questions:
            info = self.getQuestionInfo(question)
            if info:
                # 得到问题的URL
                url = "http://iask.sina.com.cn/" + info[1]
                ans = self.page_spider.getAnswer(url)
                print self.getCurrentTime(), "当前爬取第", page_num, "的内容,发现一个问题", info[2], "回答数量", info[3]
                # 构造问题的字典,插入问题
                ques_dict = {
                    "text": info[2],
                    "questioner": info[0],
                    "date": info[4],
                    "ans_num": info[3],
                    "url": url
                }

                insert_id = self.mysql.insertData('iask_question', ques_dict)
                good_ans = ans[0]
                print self.getCurrentTime(), "保存到数据库,此问题的ID为", insert_id

                # 如果存在最佳答案,那么就插入
                if good_ans:
                    print self.getCurrentTime(), insert_id, "号问题存在最佳答案", good_ans[0]
                    # 构造最佳答案的字典
                    good_ans_dict = {
                        "text": good_ans[0],
                        "answerer": good_ans[1],
                        "date": good_ans[2],
                        "is_good": str(good_ans[3]),
                        "question_id": str(insert_id)
                    }
                    # 插入最佳答案
                    if self.mysql.insertData("iask_answers", good_ans_dict):
                        print self.getCurrentTime(), "保存最佳答案成功"
                    else:
                        print self.getCurrentTime(), "保存最佳答案失败"

                # 获得其他答案
                other_anses = ans[1]
                # 遍历每一个其他答案
                for other_ans in other_anses:
                    # 如果答案存在
                    if other_ans:
                        print self.getCurrentTime(),insert_id,"号问题存在其他答案",other_ans[0]
                        # 构造其他答案的字典
                        other_ans_dict = {
                                "text": other_ans[0],
                                "answerer": other_ans[1],
                                "date": other_ans[2],
                                "is_good": str(other_ans[3]),
                                "question_id": str(insert_id)
                                }
                        # 插入这个答案
                        if self.mysql.insertData("iask_answers", other_ans_dict):
                            print self.getCurrentTime(), "保存其他答案成功"
                        else:
                            print self.getCurrentTime(),"保存其他答案失败"

    # 主函数
    def main(self):
        f_handler = open('out.log', 'w')
        sys.stdout = f_handler
        page = open('page.txt', 'r')
        content = page.readline()
        start_page = int(content.strip()) - 1
        page.close()
        print self.getCurrentTime(), "开始页码", start_page
        print self.getCurrentTime(), "爬虫正在启动,开始爬取爱问知识人问题"
        self.total_num = 100  # 新版的页面总的页数为100
        print self.getCurrentTime(), "获取到目录页面个数", self.total_num, "个"
        if not start_page:
            start_page = self.total_num
        for x in range(1, start_page):
            print self.getCurrentTime(), "正在抓取第", start_page - x + 1, "个页面"
            try: # 这里页面的页码的格式不是按照正常的1 2 3 4，而是用了其他的算法产生页码
                self.getQuestions(start_page - x + 1)
            except urllib2.URLError, e:
                if hasattr(e, "reason"):
                    print self.getCurrentTime(), "某总页面内抓取或提取失败,错误原因", e.reason
            except Exception, e:
                print self.getCurrentTime(), "某总页面内抓取或提取失败,错误原因:", e
            if start_page - x + 1 < start_page:
                f = open('page.txt', 'w')
                f.write(str(start_page - x + 1))
                print self.getCurrentTime(), "写入新页码", start_page - x + 1
                f.close()


spider = Spider()
spider.main()
