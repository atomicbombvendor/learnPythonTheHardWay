# coding=utf-8
import ftplib
import os
import zipfile
from ftplib import FTP

ftp_server = 'ftp.morningstar.com'
ftp_user = 'OnDemandMaster'
ftp_password = 'OnDemandMasterNew1234'
ftp_port = 21
ftp_timeout = 60

# ftp folder
ftp_root_path = '/APIBackup'

local_path = "D:\data\APIBackup"


# Connect FTP
def ftp_connect():
    ftp_connected = FTP()
    try:
        ftp_connected.connect(ftp_server, ftp_port, ftp_timeout)
        ftp_connected.login(ftp_user, ftp_password)
        # print ftp_connected.getwelcome()
        print "FTP Login Success"
        return ftp_connected
    except ftplib.error_perm:
        print "Error, cannot login."
        ftp_connected.quit()
        return None


ftp_t = ftp_connect()


def download_file(local_file, remote_file):
    buff_size = 1024
    file_open = open(local_file, 'wb')  # 以写模式在本地打开文件
    # 接受服务器上的文件 并写入本地文件
    ftp_t.retrbinary('RETR ' + remote_file, file_open.write, buff_size)
    ftp_t.set_debuglevel(2)  # 关闭调试模式
    file_open.close()


def download_file_tree(LocalDir, RemoteDir):
    print "start download files"
    if not os.path.isdir(LocalDir):
        os.makedirs(LocalDir)
    ftp_t.cwd(RemoteDir)
    remote_files = ftp_t.nlst()
    print "remote files", remote_files
    for file_t in remote_files:
        if 'zip' in file_t:
            local = os.path.join(local_path, file_t)
            download_file(local, file_t)


def read_file():
    for root, dir_t, files in os.walk(local_path):
        for file_name in files:
            # print "Read " + file_name
            read_zip_113(root, file_name)


def read_zip_113(root, file_name):
    try:
        zip_file = zipfile.ZipFile(os.path.join(root, file_name))
        file_list = zip_file.namelist()
        for file_t in file_list:
            if '113' in file_t:
                # 读取的文件格式是 字符串
                content_113 = zip_file.read(file_t)
                if "SLF" in content_113:
                    print file_name

                # print("Read " + file_name + " Done")
    except zipfile.BadZipfile:
        print "Bad File " + file_name


if __name__ == '__main__':
    # ftp = ftp_connect()
    # download_file_tree(local_path, ftp_root_path)
    read_file()
