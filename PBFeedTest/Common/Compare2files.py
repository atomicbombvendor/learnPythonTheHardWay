"""
compare 2 files and out put the difference
"""
from ..refactorqa.atlasintegertest.Constant import *


def compareContent(contDev, contLive):
    sd = set(contDev)
    sl = set(contLive)
    return sd - sl, sl - sd


def initFile(on, off, notOn, notOff):
    """
    check if result files are ready and prepare compareResult file names
    :param on: summary onEv
    :param off: summary offEv
    :param notOn: which not in onEv file
    :param notOff: which not in offEv file
    :return: (True|False), notOnName, notOffName
    """
    ready = os.path.isfile(on) and os.path.isfile(off)
    for i in range(0, 100):
        tempNotOn = os.path.join(
            os.path.dirname(notOn), '{}_{}.txt'.format(
                os.path.basename(notOn).replace(".txt", ""), i))
        tempNotOff = os.path.join(
            os.path.dirname(notOff), '{}_{}.txt'.format(
                os.path.basename(notOff).replace(".txt", ""), i))
        if not os.path.exists(tempNotOff) and not os.path.exists(tempNotOn):
            return ready, tempNotOn, tempNotOff
    return False, "", ""


def compareFiles(on, off, notOn, notOff):
    ready, notOn, notOff = initFile(on, off, notOn, notOff)
    if ready:
        with open(on, 'r')as fl:
            contLive = fl.readlines()
        with open(off, 'r') as fd:
            contDev = fd.readlines()

        noLive, noDev = compareContent(contDev, contLive)

        with open(notOn, 'w') as fnl:
            fnl.writelines(list(noLive))
        with open(notOff, 'w') as fnd:
            fnd.writelines(list(noDev))


if __name__ == '__main__':
    compareFiles(onEvResult, offEvResult, onEvCompareResult, offEvCompareResult)

    pass
