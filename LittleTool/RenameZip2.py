# coding=utf-8
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import os


def getFileList(folder):
    count = 0

    # 当前目录 当前目录下的子目录 当前文件
    for root, folder, files in os.walk(folder):
        for file in files:
            if ".zip" in file:
                path_s = root
                source_z = file

                path_t = root.replace("GEDF2.0", "GEDF3")
                if not os.path.exists(path_t):
                    os.makedirs(path_t)
                target_z = file.replace('2018-11-26', '2018-11-20').replace('2018-11-27', '2018-11-20')
                count = count + 1
                print "{" + str(count) + "} Processed " + path_s + "\\" + source_z
                rename_zip(path_s + "\\", source_z, path_t + "\\", target_z)
                generate_ctrl(path_t + "\\", target_z)

# 重命名Zip包中的文件名
def rename_zip(path_s, source_z, path_t, target_z):
    source = ZipFile(path_s + source_z, 'r')
    target = ZipFile(path_t + target_z, 'w', ZIP_DEFLATED)
    for file in source.filelist:
        if '2018-11-26' not in file.filename and '2018-11-27' not in file.filename:
            # target.writestr(file.filename, source.read(file.filename))
            pass
        else:
            new_file_name = file.filename.replace('2018-11-26', '2018-11-20').replace('2018-11-27', '2018-11-20')
            target.writestr(new_file_name, source.read(file.filename))
    target.close()
    source.close()

# 生成文件的ctrl
def generate_ctrl(file_path, file_name):
    target = (file_path + file_name.replace(".zip", ".ctrl"))
    md5 = GetFileMd5(file_path + file_name)
    lines = file_name + " is ready!\r" + md5
    fp = open(target, "w")
    fp.write(lines)
    fp.close()
    print "generate ctrl: " + target

# 计算文件的MD5
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


if __name__ == "__main__":
    path = "D:\data\\atlasfeed6\GEDF2.0"
    getFileList(path)
