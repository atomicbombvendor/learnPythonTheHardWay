""" 
1. start web
    provide an api which can be called once
2. add a test suit
"""

import PBFeedTest.refactorqa.atlasintegertest.service.Processor as ps
import PBFeedTest.refactorqa.atlasintegertest.service.Runjar as jarRunner
import PBFeedTest.refactorqa.atlasintegertest.utils.TestCasePrepare as cases
import PBFeedTest.refactorqa.atlasintegertest.webservice.WebService as web
from PBFeedTest.refactorqa.atlasintegertest.command.CmpContentCmd import CmpContentCmd
from PBFeedTest.refactorqa.atlasintegertest.command.CmpSummaryCmd import CmpSummaryCmd

if __name__ == '__main__':
    web.start()
    caseList = cases.getSuit(4) + cases.getSuit(5) + cases.getSuit(6)
    print(caseList)
    cmd = [CmpSummaryCmd(), CmpContentCmd()]
    jarRunner.run('dev')
    ps.process(caseList, cmd)
