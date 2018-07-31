import subprocess
from threading import Thread

from ..Constant import *

env = 'stg'


def offEvT():
    subprocess.call('java -jar -Xms2000m -Xmx2000m -Xmn2000m -Dspring.config.location={} -Dspring.profiles.active={} {}'.format(
        offEvConfigPath, env, offEvPackage).split(" "))


def onEvT():
    subprocess.call('java -jar -Xms2000m -Xmx2000m -Xmn2000m -Dspring.config.location={} -Dspring.profiles.active={} {}'.format(
        onEvConfigPath, env, onEvPackage).split(" "))


threadOff = Thread(target=offEvT)
threadOn = Thread(target=onEvT)


def run(environment):
    global env
    env = environment
    threadOff.start()
    threadOn.start()
