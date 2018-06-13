"""
1. has a list to store json files
2. can set suit
3. has some prepared suits
4. can get suit return a list of json string
"""
import os

jsonRoot = os.path.dirname(os.path.dirname(__file__)) + "\\jsons"

suit = []
allJson = []

for file in os.listdir(jsonRoot):
    with (open(os.path.join(jsonRoot, file), 'r')) as f:
        allJson.append(f.read())


# GEDF_DailyDelta_TSO
def _getSuit1():
    l = ["GEDF_DailyDelta_TSO"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


# GEDF_DailyDelta_MarketCap
def _getSuit2():
    l = ["GEDF_DailyDelta_MarketCap"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r
    pass


# GEDF_DailyDelta_FinancialStatements
def _getSuit3():
    l = ["GEDF_DailyDelta_FinancialStatements"]
    r = set()
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.add(s)
    return list(r)


# GEDF_DailyDelta_FSPerShare
def _getSuit4():
    l = ["GEDF_DailyDelta_FSPerShare"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


# GEDF_Monthly_FinancialStatement
def _getSuit5():
    l = ["GEDF_Monthly_FinancialStatement"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


# GEDF_Monthly_FSPerShare
def _getSuit6():
    l = ["GEDF_Monthly_FSPerShare"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


# GEDF_Monthly_Market
def _getSuit7():
    l = ["GEDF_Monthly_Market"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


# GEDF_Monthly_TSO
def _getSuit8():
    l = ["GEDF_Monthly_TSO"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


# GEDF_Monthly_Reference
def _getSuit9():
    l = ["GEDF_Monthly_Reference"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


# GEDF_Delete_
def _getSuit10():
    l = ["GEDF_Delete_"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


def _default():
    l = ["GEDF_Monthly_TSO"]
    r = []
    for s in allJson:
        for n in l:
            if s.find(n) != -1:
                r.append(s)
    return r


def setSuit(number=0):
    options = {0: _default(),
               1: _getSuit1(),
               2: _getSuit2(),
               3: _getSuit3(),
               4: _getSuit4(),
               5: _getSuit5(),
               6: _getSuit6(),
               7: _getSuit7(),
               8: _getSuit8(),
               9: _getSuit9(),
               10: _getSuit10()
               }
    global suit
    suit = options[number]


def getSuit(number=0):
    setSuit(number)
    return suit


if __name__ == '__main__':
    setSuit()
    pass
