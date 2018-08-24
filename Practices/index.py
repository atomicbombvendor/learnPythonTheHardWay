# coding=utf-8
from datetime import datetime
from croniter import croniter


# cron
def is_On_time(cron_exp, check_date_time):
    if not croniter.is_valid(cron_exp):
        print cron_exp + " is bad format"
    cron_iter = croniter(cron_exp, check_date_time)
    cron_next_time = cron_iter.get_next(datetime)
    cron_prev_time = cron_iter.get_prev(datetime)

    total_seconds_prev = (cron_prev_time - check_date_time).total_seconds()
    total_seconds_next = (cron_next_time - check_date_time).total_seconds()
    # todo 当前的时间必须要和Cron表达式的表示的时间一分一秒不差吗？这里需要考虑;需要考虑cloudWatch的调度
    # todo 如果是一分钟一次，就需要考虑，相差几秒的情况。
    if total_seconds_next == 0 or total_seconds_prev == 0:
        return True
    else:
        return False


cron = "0 10,14,16 * * *"
check_date_time = datetime(2018, 8, 24, 12, 0, 0)
print cron + ">>>" + str(is_On_time(cron, check_date_time))
check_date_time = datetime(2018, 8, 24, 13, 0, 0)
print cron + ">>>" + str(is_On_time(cron, check_date_time))
check_date_time = datetime(2018, 8, 26, 14, 0, 0)
print cron + ">>>" + str(is_On_time(cron, check_date_time))
check_date_time = datetime(2018, 8, 25, 16, 0, 0)
print cron + ">>>" + str(is_On_time(cron, check_date_time))

cron = "0 2 1 * *"
check_date_time = datetime(2018, 8, 1, 2, 1, 0)
print cron + ">>>" + str(is_On_time(cron, check_date_time))
