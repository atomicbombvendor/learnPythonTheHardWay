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
    file_uploaded = []

    for main_dir, sub_dir, file_name_list in os.walk(dir_name):
        print "main_dir: " + main_dir + "; subdir length: " + str(len(sub_dir))
        for file_name in file_name_list:
            # print "file name" + file_name
            absolutePath = os.path.join(main_dir, file_name)
            for post_fix in postfix:
                if post_fix in absolutePath:
                    print "#### File {" + file_name + "} find ####"
                    file_uploaded.append(absolutePath)
                    ftp_up(ftp, ftp_root_path, absolutePath)
                    ftp.cwd(ftp_root_path)

    return file_uploaded


# Connect FTP
def ftp_connect():
    ftp_connected = FTP()
    try:
        ftp_connected.connect(ftp_server, ftp_port, ftp_timeout)
        ftp_connected.login(ftp_user, ftp_password)
        print ftp_connected.getwelcome()
        print "FTP Login Success"
        return ftp_connected
    except ftplib.error_perm:
        print "Error, cannot login."
        ftp_connected.quit()
        return None


# Upload File to FTP
# ftp_root: ftp_root path
# file: file absolute path
def ftp_up(ftp_connected, ftp_root, absolute_file):
    ftp_connected.cwd(ftp_root)
    # file relative path
    file_folder = os.path.dirname(absolute_file).replace(root, '').replace("\\", "/")
    file_name = os.path.basename(absolute_file)
    ftp_path = file_folder
    print ">>>Upload %s to %s" % (file_name, ftp_root_path + ftp_path)

    try:
        ftp_connected.cwd(ftp_root + ftp_path)
    except ftplib.error_perm:
        print ">>>Path is not exists " + ftp_path
        make_dirs(ftp_connected, ftp_root, ftp_path)

    ftp_connected.storbinary('STOR ' + file_name, open(absolute_file, 'rb'))


# ftp_root for example: /AA/BB
# dir_path need to create folder
# for example: /A/B/C
# Create Folder /AA/BB/A/B/C
def make_dirs(ftp_connected, ftp_root, dir_path):
    dirs = dir_path.replace("\\", "/").split("/")
    current_path = ftp_root
    for dir_created in dirs:
        try:
            ftp_connected.cwd(current_path + "/" + dir_created)
        except ftplib.error_perm:
            ftp_connected.mkd(current_path + "/" + dir_created)


if __name__ == '__main__':
    ftp = ftp_connect()
    print "Start to upload"
    result = upload_file(root)
    ftp.quit()
