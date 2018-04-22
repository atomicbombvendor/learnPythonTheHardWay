# coding=utf-8
import logging
import logging.config
from cloghandler import ConcurrentRotatingFileHandler

# logging.config.fileConfig("../resource/logging.conf")
#
# logger = logging.getLogger('main')
# # main consoleHandler,fileHandler
# # 用上这个就不能打印了handlers.ConcurrentRotatingFileHandler
# for i in range(1900):
#     logger.info('Test Info ' + str(i))

import pyspider
import logging
import logging.config
import cloghandler
logging.config.fileConfig("../resource/logging2.conf")

logger = logging.getLogger('root')
logger.info('Test Info ' + '999')
for i in range(1900):
    logger.info('Test Info ' + str(i))