""" 
1. start web
    provide an api which can be called once
2. add a test suit
"""

import refactorqa.atlasintegertest.service.Processor as ps
import refactorqa.atlasintegertest.service.Runjar as jarRunner
import refactorqa.atlasintegertest.utils.TestCasePrepare as cases
import refactorqa.atlasintegertest.webservice.WebService as web
from refactorqa.atlasintegertest.command.CmpContentCmd import CmpContentCmd
from refactorqa.atlasintegertest.command.CmpSummaryCmd import CmpSummaryCmd

if __name__ == '__main__':
    web.start()
    caseList = cases.getSuit(5) + cases.getSuit(6) + cases.getSuit(7) + cases.getSuit(8) + cases.getSuit(9)
    print(caseList)
    cmd = [CmpSummaryCmd(), CmpContentCmd()]
    jarRunner.run('dev')
    ps.process(caseList, cmd)
