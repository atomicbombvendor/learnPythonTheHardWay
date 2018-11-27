# coding=utf-8

# 使用了cookie
import urllib2
import cookielib

#声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
#用过handler来构建opener
opener = urllib2.build_opener(handler)

#此处的open方法同urllib2的URLopen方法，也可以传入request
response = opener.open("http://www.baidu.com")
for item in cookie:
    print 'Name='+item.name
    print 'Value='+item.value


#保存cookie到文件
#设置保存cookie的文件，同级目录下的cookie.txt
fileName = 'cookie.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(fileName)
#利用urllib2库的HttpcookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#创建一个请求，原理同urllib2的urlopen
response = opener.open("http://www.baidu.com")
#保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)

#从文件中获取cookie并访问
#创建MozillaCookieJar实例对象
cookie2 = cookielib.MozillaCookieJar()
#从文件中读取cookie内容到变量
cookie2.load('cookie.txt', ignore_expires=True, ignore_discard=True)
#创建请求的Request
req = urllib2.Request('http://www.baidu.com')
#利用urllib2的build——opener方法创建一个Opener
handler2 = urllib2.HTTPCookieProcessor(cookie2)
opener2 = urllib2.build_opener(handler2)
response2 = opener2.open(req)
print response2.read()


