import refactorqa.atlasintegertest.service.Compare as cp
from refactorqa.atlasintegertest.command.Command import Command


class CmpSummaryCmd(Command):
    def execute(self):
        cp.unzipAll()
        cp.getSummary()
        cp.compareSummaryCont()
        print("comparing summary")
        pass
