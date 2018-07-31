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
    # select file number to generate Feed.
    caseList = cases.getSuit(13)
    print(caseList)
    cmd = [CmpSummaryCmd(), CmpContentCmd()]
    # select environment
    jarRunner.run('stg')
    ps.process(caseList, cmd)
