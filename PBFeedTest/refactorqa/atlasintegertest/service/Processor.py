import shutil
import sys
from time import sleep

from ..webservice import WebService as web
from ..Constant import *


def compare(cmd):
    print("Comparing")
    for c in cmd:
        c.execute()
    print("Compare finished")
    pass


def clean():
    if os.path.isdir(onEvComparePath):
        shutil.rmtree(onEvComparePath)

    if os.path.isdir(offEvComparePath):
        shutil.rmtree(offEvComparePath)
    print("Cleaned Data Feed")


def cleanSummary():
    """
    not used ye
    :return: 
    """
    if os.path.exists(onEvResult):
        os.remove(onEvResult)
    if os.path.exists(offEvResult):
        os.remove(offEvResult)

    print("Cleaned Summary")
    pass


def process(caseList, cmd):
    for case in caseList:
        web.setOnEvReturn(case)
        # make sure jar get the schedule
        sleep(15)
        while True:
            sleep(2)
            if not web.getOnEvProcessState():
                break

        web.setOffEvReturn(case)
        sleep(15)
        while True:
            sleep(2)
            if web.getOnEvProcessState():
                raise RuntimeError("State Error: Both jars are running")
            if not web.getOffEvProcessState():
                break
        compare(cmd)
        clean()
    print("Finished All")
    sleep(10)
    pass
