from ..service import Compare as cp
from Command import Command


class CmpSummaryCmd(Command):

    def __init__(self):
        pass

    def execute(self):
        cp.unzipAll()
        cp.getSummary()
        cp.compareSummaryCont()
        print("comparing summary")
        pass
