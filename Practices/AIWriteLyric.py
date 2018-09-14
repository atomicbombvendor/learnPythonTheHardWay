# coding=utf-8
import requests

import jieba

import re

from xpinyin import Pinyin

p = Pinyin()

RhymeIndex = [('1', ['a', 'ia', 'ua']), ('2', ['ai', 'uai']), ('3', ['an', 'ian', 'uan']),

              ('4', ['ang', 'iang', 'uang']), ('5', ['ao', 'iao']), ('6', ['e', 'o', 'uo']), ('7', ['ei', 'ui']),

              ('8', ['en', 'in', 'un']), ('9', ['eng', 'ing', 'ong', 'iong']), ('10', ['er']), ('11', ['i']),

              ('12', ['ie', 'ye']), ('13', ['ou', 'iu']), ('14', ['u']), ('16', ['ue']), ('15', ['qu', 'xu', 'yu'])]

RhymeDct = {'ui': '7', 'uan': '3', 'ian': '3', 'iu': '13', 'en': '8', 'ue': '16', 'ing': '9', 'a': '1', 'ei': '7',

            'eng': '9', 'uo': '6', 'ye': '12', 'in': '8', 'ou': '13', 'ao': '5', 'uang': '4', 'ong': '9', 'ang': '4',

            'ai': '2', 'ua': '1', 'uai': '2', 'an': '3', 'iao': '5', 'ia': '1', 'ie': '12', 'iong': '9', 'i': '11',

            'er': '10', 'e': '6', 'u': '14', 'un': '8', 'iang': '4', 'o': '6', 'qu': '15', 'xu': '15', 'yu': '15'}

"""
代码来源： https://blog.csdn.net/qq_42156420/article/details/82191714
分好的词与押韵表对应起来，举个栗子，比如“没有”对应的是“7-13”，
就等于你给每个词都贴了一个标签，这样你以后想搜索的时候，
就可以根据标签找到这些词了。
"""
def _analysis_words(words):
    word_py = p.get_pinyin((u'{}'.format(words)))
    lst_words = word_py.split('-')
    r = []
    for i in lst_words:
        while True:
            if not i:
                break
            token = RhymeDct.get(i, None)
            if token:  # 如果i在RhymeDct中找不到，表示没有这个韵脚
                r.append(token)
                break
            i = i[1:]  # 当前的拼音找不到韵脚，就排除第一个，用剩下的字符继续查找韵脚
    if len(r) == len(words):
        return '-'.join(r)


print(_analysis_words('兄弟'.decode('utf-8')))
