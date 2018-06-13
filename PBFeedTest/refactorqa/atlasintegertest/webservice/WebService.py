"""
1. has a flag which marks the state of processing
    builder will call api every 10 seconds if not generating any feed
2. has 2 apis, one for onEv one for offEv
3. method to set return 
4. can stop service
"""

from threading import Thread

import OffEvWebService as off
import OnEvWebService as on


def offEvT():
    off.run()


def onEvT():
    on.run()


def start():
    threadOffEv.start()
    threadOnEv.start()


def getOnEvState():
    return on.getState()


def getOnEvProcessState():
    return on.processing


def getOffEvProcessState():
    return off.processing


def getOffEvState():
    return off.getState()


def setOnEvReturn(r):
    on.setReturn(r)


def setOffEvReturn(r):
    off.setReturn(r)


def stopService():
    """
    Want to stop the web service 
    It doesn't works, haven't figure it out yet
    """
    threadOnEv.join(10)
    threadOffEv.join(10)
    pass


threadOnEv = Thread(target=onEvT)
threadOffEv = Thread(target=offEvT)

if __name__ == '__main__':
    start()
    pass
