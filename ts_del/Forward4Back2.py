# coding=utf-8

"""
需求：小芳的妈妈每天给她2.5元钱，她都会存起来，但是，
    每当这一天是存钱的第5天或者5的倍数的话，她都会花去6元钱，
    请问，经过多少天，小芳才可以存到100元钱。
"""


def forward_4_back_2(target):
    day = 0
    money_get = 2.5
    money_use = 6
    money_all = 0
    while money_all < target:
        day = day + 1
        money_all += money_get
        if (day >= 5) and (day % 5 == 0):
            money_all = money_all - money_use
        print "Day:%d money:%.1f " % (day, money_all)
    print "Day is " + str(day)


forward_4_back_2(100)
