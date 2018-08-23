import ftplib
import os

from ftplib import FTP


ftp_server = 'ftp.morningstar.com'
ftp_user = 'OnDemandMaster'
ftp_password = 'OnDemandMasterNew1234'
ftp_port = 21
ftp_timeout = 60
ftp_root_path = '/Equity2/Test/DailyDelta'

# root = "D:/GEDataFeed/DailyDelta"
root = "Y:/GeDataFeed/GEDF2.0/DailyDelta"


def upload_file(dir_name):
    print "Start to read folder " + root
    postfix = ['2018-08-06.zip', '2018-08-06.ctrl']
    result = []

    for maindir, subdir, file_name_list in os.walk(dir_name):
        print "maindir " + maindir + " subdir length " + str(len(subdir))
        for file_name in file_name_list:
            # print "file name" + file_name
            absolutePath = os.path.join(maindir, file_name)
            for post_fix in postfix:
                if post_fix in absolutePath:
                    print "#### File {" + file_name + "} find ####"
                    result.append(absolutePath)
                    ftp_up(ftp, ftp_root_path, absolutePath)
                    ftp.cwd(ftp_root_path)

    return result


# Connect FTP
def ftp_connect():
    ftp = FTP()
    try:
        ftp.connect(ftp_server, ftp_port, ftp_timeout)
        ftp.login(ftp_user, ftp_password)
        print ftp.getwelcome()
        print "FTP Login Success"
        return ftp
    except ftplib.error_perm:
        print "Error, cannot login."
        ftp.quit()
        return None


# Upload File to FTP
# ftp_root: ftp_root path
# file: file absolute path
def ftp_up(ftp, ftp_root, file):
    ftp.cwd(ftp_root)
    # file relative path
    file_folder = os.path.dirname(file).replace(root, '').replace("\\", "/")
    file_name = os.path.basename(file)
    ftp_path = file_folder
    print "Upload %s to %s" % (file_name, ftp_root_path + ftp_path)

    try:
        ftp.cwd(ftp_root + ftp_path)
    except ftplib.error_perm:
        print "Path is not exists " + ftp_path

    ftp.storbinary('STOR ' + file_name, open(file, 'rb'))


if __name__ == '__main__':
    ftp = ftp_connect()
    print "Start to upload"
    result = upload_file(root)
    ftp.quit()
