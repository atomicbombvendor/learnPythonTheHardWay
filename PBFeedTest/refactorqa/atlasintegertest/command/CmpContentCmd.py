
from ..service import Compare as cp
from ..Constant import *
from Command import Command


class CmpContentCmd(Command):
    """
    this command con only fit for ATLAS Feed
    """

    def __init__(self):
        pass

    def execute(self):
        print("comparing usa content")
        cp.unzipAll()
        fd = r"/QAData/on/data/feed/file/GEDF2.0//"
        if os.path.exists(fd):
            feedType = os.listdir(fd)
            for tp in feedType:
                ls = cp.getFileList(os.path.join(fd, tp, "USA"))
                with open(os.path.join(compareResult, "USA.txt"), 'a') as g:
                    for file in ls:
                        fileOff = file.replace(os.path.join('QAData', 'on'), os.path.join('QAData', 'off'))
                        flag, route = cp.compare2Files(file, fileOff)
                        if not flag:
                            g.write(route + '\n')
