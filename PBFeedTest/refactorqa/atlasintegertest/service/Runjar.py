import subprocess
from threading import Thread

from refactorqa.atlasintegertest.Constant import *

env = 'stg'


def offEvT():
    subprocess.call('java -jar -Xms4g -Xmx4g -Xmn2g -Dspring.config.location={} -Dspring.profiles.active={} {}'.format(
        offEvConfigPath, env, offEvPackage).split(" "))


def onEvT():
    subprocess.call('java -jar -Xms4g -Xmx4g -Xmn2g -Dspring.config.location={} -Dspring.profiles.active={} {}'.format(
        onEvConfigPath, env, onEvPackage).split(" "))


threadOff = Thread(target=offEvT)
threadOn = Thread(target=onEvT)


def run(environment):
    global env
    env = environment
    threadOff.start()
    threadOn.start()
