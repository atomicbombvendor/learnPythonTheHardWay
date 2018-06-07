from ..Constant import *


def getInfo(r, file):
    msg_ = os.path.join(r, file)

    if msg_[-5:] == '.ctrl':
        finalMsg_ = msg_
    else:
        finalMsg_ = '{}   size:{}'.format(msg_, str(os.path.getsize(msg_)))
    for i in filters:
        finalMsg_ = finalMsg_.replace(i, 'boooom')
    return finalMsg_


def getDir(r, g):
    for r_, d_, f_ in os.walk(r):
        for file_ in f_:
            msg_ = getInfo(r_, file_)
            g.write('{}\n'.format(msg_))


if __name__ == '__main__':
    rstlocation = r'D:/QA/dmc'
    root = r'D:/QA/dmc/dmc_live'

    with open(os.path.join(rstlocation, 'rstlive.txt'), 'w') as f:
        getDir(root, f)
