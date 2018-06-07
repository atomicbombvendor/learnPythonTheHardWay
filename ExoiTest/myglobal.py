from ExoiTest.LogSingleton import LogSingleton

# logger
# logger = LogSingleton().get_logger()


# def _init():
#     global logger
#     logger = LogSingleton().get_logger()


def get_logger():
    # logger = None
    # if logger is None:
    #     logger = LogSingleton().get_logger()
    #     return logger
    # else:
    #     return logger
    return LogSingleton().get_logger()


