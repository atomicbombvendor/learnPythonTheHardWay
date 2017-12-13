import ConfigParser
import os


class ConfigUtil:
    def __init__(self):
        os.chdir("..\config")
        self.util = ConfigParser.ConfigParser()
        self.util.read("config.config")

    def get_key_value(self, section, option):
        return self.util.get(section, option)

    def sections(self):
        return self.util.sections()

    def options(self, option):
        return self.util.options(option)

    def items(self, section):
        return self.util.items(section)


# cfUtil = ConfigUtil()
#
# # return all section
# secs = cfUtil.sections()
# print 'sections:', secs, type(secs)
# opts = cfUtil.options('tieba')
# print 'options:', opts, type(opts)
# kvs = cfUtil.items('tieba')
# print 'k-v:', kvs
#
# # read by type
# tieba_seeLZ = cfUtil.get_key_value('tieba', 'seeLZ')
# tieba_pageNum = cfUtil.get_key_value('tieba', 'pageNum')
# tieba_floorTag = cfUtil.get_key_value('tieba', 'floorTag')
# tieba_url = cfUtil.get_key_value('tieba', 'tieba_url')
# print "tieba_seeLZ:", tieba_seeLZ
# print "tieba_pageNum:", tieba_pageNum
# print "tieba_floorTag:", tieba_floorTag
# print "tieba_url:", tieba_url