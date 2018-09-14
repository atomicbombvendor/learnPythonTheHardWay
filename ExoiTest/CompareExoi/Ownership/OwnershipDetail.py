# coding=utf-8
import json

import jsonpath

from ExoiTest.CompareExoi.AbstractEXOI import AbstractEXOI
from ExoiTest.CompareExoi.Ownership.Ownership import Ownership


class OwnershipDetail(Ownership):

    def __init__(self):
        AbstractEXOI.__init__(self)
        Ownership.__init__(self)
        self.value_mapping = {
            44007: 'currencyId', # Always USD for ownertype 2 &3
            44000: 'filerCIK',
            44001: 'ownerName',
            44002: 'numberOfShares',
            44003: 'marketValue',
            44004: 'shareChange',
            44005: 'percentageInPortfolio',
            44006: 'percentageOwnership',
        }

    def construct_url(self, param):
        performanceId = param['performanceId']
        ownerType = param['ownerType']
        issue_id = self.issueId.get_issueId(performanceId)
        issue_id_part = ''
        if ownerType == 2:
            issue_id_part = "%s/institution" % issue_id
        elif ownerType == 3:
            issue_id_part = "%s/mutual-fund" % issue_id
        else:
            self.log_exoi.error("Error ownerType " + ownerType + " >>> " + str(param))
        return (self.init_url + issue_id_part).encode('utf-8')

    def parse_line(self, line_value):
        param = {}

        values = line_value.split("|")
        param['performanceId'] = values[0]
        param['dataId'] = int(values[1])
        param['dataValue'] = values[2]
        param['asOfDate'] = values[3]
        param['ownerType'] = int(values[4])
        param['ownerId'] = values[5]
        return param

    def check_value(self, line_value):
        flag = False

        if not self.content or self.content == '':
            return flag

        values = self.parse_line(line_value)
        asOfDate = values['asOfDate']
        ownerId = values['ownerId']

        ownership_object = json.loads(self.content)
        data_name = self.value_mapping[values['dataId']]
        if data_name == 'currencyId' and self.get_value(value_set=values) == 'USD':
            flag = True
        else:
            # from dat file
            data_value_expect = self.get_value(value_set=values)
            # from ownership
            path = "$.ownershipData.owners[?(@.asOfDate=='%s' and @.ownerId=='%s')][%s]" % (asOfDate, ownerId, data_name)
            data_value_real = jsonpath.jsonpath(ownership_object, path)[0]

            if AbstractEXOI.compare_value(data_value_expect, data_value_real):
                flag = True

            try:
                self.log_exoi.info(
                    "%s %s api:%s|file:%s" % (
                        str(values['dataId']), data_name, str(data_value_real.encode), str(data_value_expect)))
            except Exception, e:
                if "'int' object has no attribute 'encode'" in e.message:
                    self.log_exoi.info(
                        "%s %s api:%s|file:%s" % (
                            str(values['dataId']), data_name, data_value_real, str(data_value_expect)))
                else:
                    self.log_exoi.info(
                        "%s %s api:%s|file:%s" % (
                            str(values['dataId']), data_name, data_value_real.encode('utf-8'), str(data_value_expect)))

        return flag

    # 需要有特殊的操作的DataId
    def get_value(self, value_set):
        dataId = value_set['dataId']
        return value_set['dataValue']
