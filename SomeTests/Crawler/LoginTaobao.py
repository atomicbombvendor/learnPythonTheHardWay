# coding=utf-8
# 博客连接： https://cuiqingcai.com/1076.html
import urllib
import urllib2
import cookielib
import re
import webbrowser
import taobaoTool


# 模拟登陆淘宝
class Taobao:
    def __init__(self):
        self.loginURL = "https://login.taobao.com/member/login.jhtml"

        self.proxyURL = "http://120.193.146.97:843"

        self.loginHeaders = {
            'Host': 'login.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Referer': 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive'
        }

        self.userName = 'tb46233_2013'
        # ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '099#KAFEq7ErEW4E6YTLEEEEE6twSciMA6twSriFD6tqDyJFZIYBDcBE+fPHYRvFV6N3YrwIgfAcYsxjgftwYsJICIzJgsXjG1qTETiL/3iDaf+VspJLY9pjAM3fY68O8ObTETOLros3Z9lP/caIDtf632JLvfZJt68Vvt+CL0qTETBL/3iSEHZiWRnGetsK40lxL6hjab1iE7EmQsaStET6Xc+tdp/XC0h9SUaj4osE4GFEHXcdt37Ej5JU/91Onb8jvtpqS0JcGTdTEEi5DEEEJGFET6i5EE1iE7EmQsaStEEDer+tdp/XC0h9SUaj4osEJGFET6i5EE1sE7EqsyvXnuLlsyabu15NIGFETrZdt37UVVqTETBL/3iSlC7mWRnGetsK40lxL6hjabEnE7EmQyNyk+alsyLWte/QaMh0DMsW8u8A6GFE1XZV6LyRluZlp+qTETiL/9iSTThVspJLY9pjAM3fY68O8z5TEEiP/3BGTGFETrZtt3illW4TEHREQl3mihTy+EP05c6o3mvkLmoYtZG+1DvkLmyU0He6mdeI2/ob06y6mStrLLKoDNvkLm2IRhikLHf3p2o+RKA3kfMV+wdZaqZqLLL46aMRvfP2gGFEePjyEI/qaWw7zVZBNdZ6bteWNweGL5eDZ/e0Ps0twyJoPPqVNdZ6bteWNw5SaGZQgW9BPzQp3rkJrV50h3VlubngDjCo/slvS3ORHAOlxr1wV6XAhgwwgrr1zwcXaQZ4YeywqOjc1s9wYfq8vba3U61vYg829YRAGuJiIVIulu2YUtxsHddprt8DZgXAL7nAGuJiIai3aWiBsbhBrQu3uUWDZLhGLiZnZR8kO7FEpcZdt3illuZdsyaaolllsviP/36alllzgcZddn3llu8bsyaaMlllW0C/E7EhsOaZttwMJ7FE1cZdt0kxYAs9/GFETIZ4gbq9E7EFD67EEp5TEEi5D7EE6GFEHucVqw1aluZtDl2OuPhgLP99sQwga2hcrGFEhrcVqw1sluZdsySCq+mV/q8FnVuPxoZqCIi9JGFET6i5EEEnE7EKsyN3iYwlsyd06GFEHXhV0hmQluZQZ92OuqZT8fkcuz/zbjdTEEi5DEEEIGFEHccdt37UUsvbUXcTdzJHYtZEZ2r2IGFETrZtt35jI1qTETiL/9iDFX1VspJLY9pjAM3fY68O8zqTETBL/3iSEw5aWRnGetsK40lxL6hjab1iE7EmQsaStEEV1c+tdp/XC0h9SUaj4osE4GFEHXcdt37E3k3U/91Onb8jvtpqS0JcGKqTETBL/3iSEFJHWRnGetsK40lxL6hjab1iE7EmQsaStETH2c+tdp/XC0h9SUaj4osE4GFEHXcdt37E5XwU/91Onb8jvtpqS0JcGKqTETBL/3iSEHHiWRnGetsK40lxL6hjab1sE7E2QsvFAfwlsyabVuwYiiZgQVL34XcDYMw0bUS9E7EFD67EEKqTETBL/3iSEJJ7WRnGetsK40lxL6hjab1iE7EmQsaStETDku+tdp/XC0h9SUaj4osErGFEhrcVCbrxluZds1seW+mV/b83S0nzxoZqCIi9'
        # 密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '7016289f63aac2841a988f45d2a4975c2c1feebd6332d22d7070c97e2525d8bc174f01a208999aec86f621dee5efbbe47b8ffc93fa4edca7dfe1a348c78e5a750c9c75ad0e82626532f5f6e5e344e0b4c41c8c1ca5704a89640193da4f273bfb922f58c0422fae8acd5f685fd38f40d3d6cdb6c5b41fe3f4ae79f4bc3dca17a3'

        self.post = post = {
            'TPL_username': self.userName,
            'TPL_password': '',
            'ncoSig': '',
            'ncoSessionid': '',
            'ncoToken': '4d16fa510b53a91979cb2a28b7da15b222d1f0d0',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': '0',
            'newlogin': '0',
            'TPL_redirect_url': 'https://www.taobao.com/',
            'from': 'tbTop',
            'fc': 'default',
            'style': 'default',
            'css_style': '',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'tid': '',
            'loginType': '3',
            'minititle': '',
            'minipara': '',
            'pstrong': '',
            'sign': '',
            'need_sign': '',
            'isIgnore': '',
            'full_redirect': '',
            'sub_jump': '',
            'popid': '',
            'callback': '',
            'guf': '',
            'not_duplite_str': '',
            'need_user_id': '',
            'poy': '',
            'gvfdcname': '10',
            'gvfdcre': '68747470733A2F2F7777772E74616F62616F2E636F6D2F',
            'from_encoding': '',
            'sub': '',
            'TPL_password_2': self.password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'allp': '',
            'oslanguage': 'zh-CN',
            'sr': '1920*1080',
            'osVer': '',
            'naviVer': 'firefox|57',
            'osACN': 'Mozilla',
            'osAV': '5.0+(Windows)',
            'osPF': 'Win64',
            'miserHardInfo': '',
            'appkey': '',
            'nickLoginLink': '',
            'mobileLoginLink': self.loginURL,
            'showAssistantLink': '',
            'ua': self.ua}
        # 将POST的数据进行编码转换
        self.postData = urllib.urlencode(self.post)
        # 设置代理
        self.proxy = urllib2.ProxyHandler({'http': self.proxyURL})
        # 设置cookie
        self.cookie = cookielib.LWPCookieJar()
        # 设置cookie处理器
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        # 设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib2.build_opener(self.cookieHandler, self.proxy, urllib2.HTTPHandler)

        self.newCookie = cookielib.CookieJar()
        self.newOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.newCookie))

        self.tool = taobaoTool.Tool()
        self.J_HToken = ''

    # 得到是否需要输入验证码，这次请求有时会需要验证码
    def needIdenCode(self):
        # 第一次登录获取验证码尝试，构建request
        request = urllib2.Request(self.loginURL, self.postData, self.loginHeaders)
        # 得到第一次登录尝试的相应
        response = self.opener.open(request)
        # 获取其中的内容
        content = response.read().decode('gbk')
        # 获取状态吗
        status = response.getcode()
        # 状态码为200，获取成功
        if status == 200:
            print u"获取请求成功"
            # \u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801', re.S)
            result = re.search(pattern, content)
            if result:
                print u"此次安全验证需要输入验证码"
                return content
            else:
                print u"此次安全验证通过，您这次不需要输入验证码"
                return False
        else:
            print u"获取请求失败"

    def getIdenCode(self, page):
        # 得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"', re.S)
        matchResult = re.search(pattern, page)
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容"
            return False

    def loginWithCheckCode(self):
        checkCode = raw_input("请输入验证码:")
        self.post['TPL_checkCode'] = checkCode

        self.postData = urllib.urlencode(self.post)

        try:
            request = urllib2.Request(self.loginURL, self.postData, self.loginHeaders)
            response = self.opener.open(request)
            content = response.read().decode("GBK")
            # 检测验证码错误的正则表达式，\u9a8c\u8bc1\u7801\u9519\u8bef 是验证码错误五个字的编码
            pattern = re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef', re.S)
            result = re.search(pattern, content)

            if result:
                print u"验证码输入错误"
                return False
            else:
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern, content)
                if tokenMatch:
                    print u"验证码输入正确"
                    print tokenMatch.group(1)
                    self.J_HToken = tokenMatch.group(1)
                    return False
        except urllib2.HTTPError, e:
            print u"连接服务器错误，原因", e.reason
            return False

    @staticmethod
    def getSTbyToken(token):
        tokenURL = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % token
        request = urllib2.Request(tokenURL)
        response = urllib2.urlopen(request)

        pattern = re.compile('{"st":"(.*?)"}', re.S)
        result = re.search(pattern, response.read())

        if result:
            print u"成功获取st码"
            st = result.group(1)
            return st
        else:
            print u"未匹配到ST"
            return False

    def loginByST(self, st, userName):
        stURL = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st, userName)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive'
        }
        request = urllib2.Request(stURL, headers)
        # newOpener 保存了这次登陆的Cookie
        response = self.newOpener.open(request)
        content = response.read().decode('GBK')

        pattern = re.compile('top.location = "(.*?)"', re.S)
        match = re.search(pattern, content)
        if match:
            print u"登录网址成功"
            location = match.group(1)
            return True
        else:
            print "登录失败"
            return False

    def getGoodsPage(self, pageIndex):
        goodsURL = 'http://buyer.trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1&pageNum=' + str(
            pageIndex)
        goodsURL2 = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'
        if self.J_HToken:
            response = self.newOpener.open(goodsURL)
            page = response.read().decode("GBK")
            return page
        else:
            print u"Token为空,直接获取内容"
            response = self.opener.open(goodsURL2)
            page = response.read().decode("GBK")
            return page

    def getAllGoods(self, pageNum):
        print u"商品的列表如下"
        for x in range(1, int(pageNum) + 1):
            page = self.getGoodsPage(x)
            self.tool.getGoodsInfo(page)

    def main(self):
        needResult = self.needIdenCode()
        if not (needResult is False):  # 为False为假，可能有值，但不为False
            print u"您需要手动输入验证码"
            idenCode = self.getIdenCode(needResult)
            # 得到了验证码的链接
            # 得到了验证码的链接
            if not idenCode == False:
                print u"验证码获取成功"
                print u"请在浏览器中输入您看到的验证码"
                webbrowser.open_new_tab(idenCode)
                J_HToken = self.loginWithCheckCode()
                print "J_HToken", J_HToken
            # 验证码链接为空，无效验证码
            else:
                print u"验证码获取失败，请重试"
        else:
            print u"不需要输入验证码"

        if not self.J_HToken:
            page = self.getGoodsPage(1)
            pageNum = self.tool.getPageNum(page)
            self.getAllGoods(pageNum)
        else:
            st = self.getSTbyToken(self.J_HToken)
            result = self.loginByST(st, self.userName)
            if result:
                page = self.getGoodsPage(1)
                pageNum = self.tool.getPageNum(page)
                self.getAllGoods(pageNum)


taobao = Taobao()
taobao.main()
