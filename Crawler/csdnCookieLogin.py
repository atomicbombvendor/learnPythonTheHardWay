# coding=utf-8

import urllib2
import cookielib
import urllib
from bs4 import BeautifulSoup

fileName = 'csdnCookie.txt'
cookie = cookielib.MozillaCookieJar(fileName)
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

loginUrl = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"

#登陆前准备
response = opener.open(loginUrl)
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
    '_eventId:': "submit"
}

postData = urllib.urlencode(values)

opener.addheaders = [("User-Agent",
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36")]

result = opener.open(loginUrl, postData)

cookie.save(ignore_expires=True, ignore_discard=True)

print result
print "###############################"

#利用Cookie访问另一个网址,个人中心
userInfo = 'http://my.csdn.net/my/mycsdn'
result = opener.open(userInfo)
print result.read()