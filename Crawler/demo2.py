# coding=utf-8
## UrlLib库的高级用法

import urllib
import urllib2

enable_proxy = True
proxy_handler = urllib2.ProxyHandler({'http': 'http://some-proxy.com:8080'})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)

urllib2.install_opener(opener)

url = 'http://www.server.com/login'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'username': 'cqc', 'password': 'xxx'}
headers = {'user-Agent': user_agent, 'Referer': 'http://www.zhihu.com/articles'}
data = urllib.urlencode(values)
request = urllib2.Request(url, data, headers)
response = urllib2.urlopen(request, timeout=10)
page = response.read()
print page


# Send PUT and Delete
request = urllib2.Request(url, data=data)
request.get_method = lambda: 'PUT'  # or 'DELETE' 这是一个匿名函数，覆盖了get_method方法
response = urllib2.urlopen(request)

# Debug log
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.baidu.com')

