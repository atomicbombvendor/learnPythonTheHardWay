# coding=utf-8
import re
import urllib2
from datetime import datetime

from ExoiTest import myglobal
from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI


class CurrencyExchangeRate(AbstractEXOI):

    def __init__(self):
        AbstractEXOI.__init__(self)
        self.log_exoi = myglobal.get_logger()
        self.value_mapping = {
            33000: 'ClosePrice'
        }
        self.init_url = 'http://tstool.morningstar.com/interface/NewWindow.aspx?Server=Production&objectid=CU$$$$$%s&tstype=1575&table=base'

    def get_content(self, param):
        try:
            intact_url = self.construct_url(param)
            request = urllib2.Request(intact_url)
            response = urllib2.urlopen(request)

            starttime_1 = datetime.now()
            content = response.read()
            endtime_1 = datetime.now()
            self.log_exoi.info("Read URL take %dms" % ((endtime_1-starttime_1).microseconds / 1000))

            starttime_2 = datetime.now()
            processed_content = self.filter_tag(content)
            endtime_2 = datetime.now()
            self.log_exoi.info("Filter html content take %dms" % ((endtime_2 - starttime_2).microseconds / 1000))

            self.content = processed_content
        except urllib2.HTTPError, e:
            print e

    # 检查传入的记录的值可以可以在xml中找到
    def check_value(self, line_value):
        flag = False
        line_value_set = self.parse_line(line_value)
        target_AsOf = line_value_set['AsOf']
        target_ClosePrice = line_value_set['ClosePrice'] # float
        target_CurrenyId = line_value_set['CurrencyId']

        startTime = datetime.now()
        currencyId = self.get_CurrencyId(self.content)
        dict_ClosePrice = self.get_Date_ClosePrices(self.content)
        endtime = datetime.now()
        self.log_exoi.info("Find value from html take %dms" % ((endtime - startTime).microseconds / 1000))

        if abs(dict_ClosePrice[target_AsOf] - target_ClosePrice) < 0.0001 and currencyId in target_CurrenyId:
            flag = True
        return flag

    # 过滤HTML页面，去除一些标签
    def filter_tag(self, htmlStr):
        # ObjectID:<td colspan=2>(CU\$\$\$\$\$[A-Z]{3})<th
        #
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        # re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_font_start = re.compile('<font[^>]*?>', re.I) # font标签
        re_font_end = re.compile('</font>', re.I)  # font标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        re_VIEWSTATE = re.compile('<input.*?id="__VIEWSTATE"[^>]*/>')  # Id=VIEWSTATE的input标签
        re_a = re.compile('<a[^>]*>')
        re_a2 = re.compile('</a>')
        s = re_cdata.sub('', htmlStr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        # s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_font_start.sub('', s)
        s = re_font_end.sub('', s)
        s = re_comment.sub('', s)  # 去掉HTML注释
        s = re_VIEWSTATE.sub('', s)  # 去掉Id=VIEWSTATE的input标签
        s = re_a.sub('', s)
        s = re_a2.sub('', s)
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        s = self.replaceCharEntity(s)  # 替换实体

        s = s.replace("</td><td>", "@@")

        return s

    # def filter_tag2(self, content):


    # 替换常用HTML字符实体.
    # 使用正常的字符替换HTML中特殊的字符实体.
    # 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    # @param htmlstr HTML字符串.
    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"',
                         '': '@@'}

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)

        while sz:
            entity = sz.group()  # entity全称，如&gt;
            key = sz.group('name')  # 去除&;后entity,如&gt;为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    # 解析line，找出拼接URL需要的参数
    def parse_line(self, line_value):
        param = {'CurrencyId': '',
                 'DataPoint': '',
                 'ClosePrice': '',
                 'AsOf': '',
                 'USD': 'USD'}

        values = line_value.split("|")
        param['CurrencyId'] = values[0]
        param['DataPoint'] = values[1]
        param['ClosePrice'] = float(values[2])
        param['AsOf'] = values[3]
        param['USD'] = values[4]
        # AMD | 33000 | 507.61421 | 2018 - 05 - 19 | USD
        return param

    # 产生完整的URL
    def construct_url(self, param):
        intact_url = self.init_url % (param['CurrencyId'])
        return intact_url

    def get_CurrencyId(self, content):
        return re.search("ObjectID:<td colspan=2>CU\$\$\$\$\$([A-Z]{3})<th",
                               content).group(1)

    def get_Date_ClosePrices(self, content):
        date_currencys = re.findall("<tr><td>(.*?)</td></tr>", content)
        currency_set = {}  # 字典
        for date_currency in date_currencys:
            date = date_currency.split("@@")[0]
            currency = float('%.5f' % (1 / float(date_currency.split("@@")[1])))
            currency_set[date] = currency
        return currency_set