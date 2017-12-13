import ConfigParser
import os

os.chdir("..\config")

cf = ConfigParser.ConfigParser()

cf.read("config.config")

# return all section
secs = cf.sections()
print 'sections:', secs, type(secs)
opts = cf.options('tieba')
print 'options:', opts, type(opts)
kvs = cf.items('tieba')
print 'k-v:', kvs

# read by type
tieba_seeLZ = cf.get('tieba', 'seeLZ')
tieba_pageNum = cf.getint('tieba', 'pageNum')
tieba_floorTag = cf.get('tieba', 'floorTag')
tieba_url = cf.get('tieba', 'tieba_url')
print 