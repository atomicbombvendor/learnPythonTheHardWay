import zipfile

import os


def unzipFile(r, f):
    f_ = zipfile.ZipFile(os.path.join(r, f))
    f_.extractall(os.path.join(r, f.replace('.zip', '')))


def deleteFile(r, f):
    os.remove(os.path.join(r, f))


def walkFile(r, f):
    unzip(os.path.join(r, f.replace('.zip', '')))


def unzip(r):
    for r_, d_, f_ in os.walk(r, topdown=True):
        for file_ in f_:
            if file_[-4:] == '.zip':
                unzipFile(r_, file_)
                deleteFile(r_, file_)
                walkFile(r_, file_)


if __name__ == '__main__':
    root = r'D:\QA'
    unzip(root)
