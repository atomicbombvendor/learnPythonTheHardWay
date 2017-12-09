# coding=utf-8
# coding = utf-8
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

filename = 'cookie_csdn.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
# 通过handler来构建opener
opener = urllib2.build_opener(handler)

loginurl = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"

# 登陆前准备：获取lt和exection
response = opener.open(loginurl)
soup = BeautifulSoup(response.read(), "lxml")
for input in soup.form.find_all("input"):
    if input.get("name") == "lt":
        lt = input.get("value")
    if input.get("name") == "execution":
        execution = input.get("value")

# post信息
values = {
    'username': 'xieyuepinran51437@163.com',
    'password': 'chunchunj',
    "lt": lt,
    "execution": execution,
    "_eventId": "submit"
}

postdata = urllib.urlencode(values)

opener.addheaders = [("User-Agent",
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36")]

# 模拟登录,保存cookie到cookie.txt中
result = opener.open(loginurl, postdata)

cookie.save(ignore_discard=True, ignore_expires=True)

print result
print "###############################"
# 登陆后我们随意跳转到博客
url = "http://my.csdn.net/my/mycsdn"
result = opener.open(url)
print result.read()
