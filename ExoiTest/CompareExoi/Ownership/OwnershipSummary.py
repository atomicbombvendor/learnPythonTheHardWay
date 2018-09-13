# coding=utf-8
from datetime import date
import jsonpath

from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from ExoiTest.CompareExoi.Ownership.Ownership import Ownership
import json


class OwnershipSummary(Ownership):

    def __init__(self):
        AbstractEXOI.__init__(self)
        Ownership.__init__(self)
        self.value_mapping = {
            41000: 'totalOwners',
            41001: 'percentageOwnership',
            41002: 'totalSharesOwned',
            41003: 'totalIncreasedShares',
            41004: 'totalDecreasedShares',
        }

    def construct_url(self, param):
        performanceId = param['performanceId']
        issue_id = self.issueId.get_issueId(performanceId)
        issue_id_part = "%s/institution/summary?start-date=2010-01-31&end-date=%s-%s-%s" % (issue_id, date.year, date.month, date.day)
        return self.init_url + issue_id_part

    def parse_line(self, line_value):
        param = {'PerformanceId': 'EquityData',
                 'Content': 'CompanyInfo',
                 'IdType': 'EquityCompanyId',
                 'Id': ''}

        values = line_value.split("|")
        param['PerformanceId'] = values[0]
        param['dataId'] = int(values[1])
        param['dataValue'] = values[2]
        param['asOfDate'] = values[3]
        param['period'] = values[4]
        return param

    def check_value(self, line_value):
        flag = False
        values = self.parse_line(line_value)
        asOfDate = values['asOfDate']
        ownership_object = json.loads(self.content)
        data_name = self.value_mapping[values['dataId']]
        # from dat file
        data_value_expect = self.get_value(value_set=values)
        # from ownership
        path = "$.ownershipData.summaries[?(@.asOfDate=='%s')][%s]" % (asOfDate, data_name)
        data_value_real = jsonpath.jsonpath(ownership_object, path)

        if AbstractEXOI.compare_value(data_value_expect, data_value_real):
            flag = True

        self.log_exoi.info(
            "%s %s api:%s|file:%s" % (
                str(values['dataId']), data_name, str(data_value_real), str(data_value_expect)))

        return flag

    # 需要有特殊的操作的DataId
    def get_value(self, value_set):
        dataId = value_set['dataId']
        if 41001 == dataId:
            return '%.4f' % (float(value_set['dataValue']) * 100.00)
        else:
            return value_set[2]
