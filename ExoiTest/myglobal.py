from ExoiTest.LogSingleton import LogSingleton

global logger
logger = LogSingleton().get_logger()


def _init():
    global logger
    logger = LogSingleton().get_logger()


def get_logger():
    global logger
    if logger is None:
        logger = LogSingleton().get_logger()
        return logger
    else:
        return logger
