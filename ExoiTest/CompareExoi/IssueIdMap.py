import codecs
import os


def read_issueId_map():
    issueId_file = os.path.abspath('..') + "\\ConfigFile\\IssueIdMap.dat"
    issueId_map2 = {}

    with codecs.open(issueId_file, 'r', 'utf-8') as content:
        for line in content:
            companyId = line.split("\t")[0]
            shareClassId = line.split("\t")[1]
            issueId = line.split("\t")[2]
            issueId_map2[shareClassId] = issueId
    return issueId_map2


class IssueId:
    issueId_map = read_issueId_map()

    def get_issueId(self, shareClassId):

        issueId = self.issueId_map[shareClassId].strip().replace("\r\n", "")

        if issueId:
            return issueId
        else:
            print "Not find issueId from %s " % shareClassId

