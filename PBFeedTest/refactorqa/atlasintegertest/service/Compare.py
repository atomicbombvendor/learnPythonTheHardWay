"""
provide some utils for comparision
"""
from ..utils import Unzipfile as unzip
from ....Common import Compare2files as cmp
from ..Constant import *
import Summary as Summary

tempOn = ''
tempOff = ''


def unzipAll():
    unzip.unzip(onEvComparePath)
    unzip.unzip(offEvComparePath)
    pass


def initFile():
    global tempOff
    global tempOn
    for i in range(0, 100):
        tempOn = os.path.join(
            compareResult, '{}_{}.txt'.format(
                os.path.basename(onEvResult).replace(".txt", ""), i))
        tempOff = os.path.join(
            compareResult, '{}_{}.txt'.format(
                os.path.basename(offEvResult).replace(".txt", ""), i))
        if not os.path.exists(tempOff) and not os.path.exists(tempOn):
            return
    else:
        raise IOError


def getSummary():
    initFile()
    with(open(tempOn, 'w')) as f:
        Summary.getDir(onEvComparePath, f)
    with(open(tempOff, 'w')) as g:
        Summary.getDir(offEvComparePath, g)
    pass


def compareSummaryCont():
    cmp.compareFiles(tempOn, tempOff, onEvCompareResult, offEvCompareResult)
    pass


def compare2Files(onEvPath, offEvPath):
    if not os.path.exists(onEvPath) or not os.path.exists(offEvPath):
        return False, onEvPath
    with (open(onEvPath, 'r')) as f:
        contOn = f.readlines()
    with (open(offEvPath, 'r')) as g:
        contOff = g.readlines()
    if not len(set(contOn) - set(contOff)) == 0:
        return False, onEvPath
    else:
        return True, onEvPath


def getFileList(folder):
    """
    get all the file path in the provided folder
    ctrl file will be filtered
    :return: file list 
    """
    ls = []
    for root, folder, files in os.walk(folder):
        for file in files:
            if not file.split(".")[-1:][0] == 'ctrl':
                ls.append(os.path.join(root, file))
    return ls
