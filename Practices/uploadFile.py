import codecs
import ftplib
import os

from ftplib import FTP

ftp_server = 'ftp.morningstar.com'
ftp_user = 'OnDemandMaster'
ftp_password = 'OnDemandMasterNew1234'
ftp_port = 21
ftp_timeout = 60

# ftp folder
# ftp_root_path = '/Equity2/DailyDelta'
ftp_root_path = '/Equity2/Test/DailyDelta'
# local path that have linked to share floder
# root = "/data/GEDF2.0/DailyDelta"
root = "Y:\GeDataFeed\GEDF2.0\DailyDelta"
# file need to upload
postfix = ['2018-08-06.zip', '2018-08-06.ctrl']
regions = []

processed_file_log = "processed_file.dat"
process_files = []

processed_region_log = "processed_region.dat"
processed_region = []

'''
Upload share floder files to FTP folder.
1. run this command on linux to link local folder to 
'sudo mount -t cifs -o credentials=/mnt/cifs.properties \\\\msnetapp601cifs94.morningstar.com\\GeDataFeed\\GEDF2.0 /data/GEDF2.0/'
2. use command 'python {this file name}'
'''

ftp = None


def upload_file(dir_name):
    global ftp
    print "Start to read folder " + root
    file_uploaded = []
    read_ftp_file_uploaded()
    prev_region = None
    current_region = None
    read_region_processed()
    read_ftp_file_uploaded()

    for main_dir, sub_dir, file_name_list in os.walk(dir_name):
        tmp = get_region(main_dir)
        current_region = tmp if tmp else None

        if current_region in processed_region and current_region in main_dir:
            continue

        if current_region and prev_region and current_region != prev_region:
            write_region(prev_region)

        print "main_dir: " + main_dir + "; subdir length: " + str(len(sub_dir)) + "; start processed " + str(
            len(regions)) + " regions."
        ftp = ftp_connect()
        for file_name in file_name_list:
            # print "file name" + file_name
            absolutePath = os.path.join(main_dir, file_name)
            for post_fix in postfix:
                if post_fix in absolutePath:
                    # print "#### File {" + file_name + "} find ####"
                    if check_file_upload(absolutePath):
                        print "** File {" + file_name + "} had uploaded **"
                    else:
                        file_uploaded.append(absolutePath)
                        # ftp_up(ftp, ftp_root_path, absolutePath)
                        log_ftp_file_uploaded(absolutePath)
                        prev_region = current_region if current_region else prev_region
                    ftp.cwd(ftp_root_path)

        write_region(current_region)

    return file_uploaded


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


def get_region(path):
    post_fix = path.replace(root, '').replace("\\", '').replace("/", "")
    if len(post_fix) == 3:
        regions.append(post_fix)
        return post_fix
    else:
        return None


def read_ftp_file_uploaded():
    global process_files
    with codecs.open(processed_file_log, "r", "utf-8") as f:
        for line in f:
            process_files.append(line)


def log_ftp_file_uploaded(absolute_file):
    file_folder = os.path.dirname(absolute_file).replace(root, '').replace("\\", "/")
    file_name = os.path.basename(absolute_file)
    ftp_path = file_folder
    with codecs.open(processed_file_log, "a", "utf-8") as f:
        f.write(ftp_root_path + ftp_path + "/" + file_name)
        f.write("\r\n")


def check_file_upload(absolute_file):
    file_folder = os.path.dirname(absolute_file).replace(root, '').replace("\\", "/")
    file_name = os.path.basename(absolute_file)
    ftp_path = file_folder
    if ftp_root_path + ftp_path + "/" + file_name in processed_file_log:
        return True
    else:
        return False


def write_region(data):
    if data:
        with codecs.open(processed_region_log, "a", "utf-8") as f:
            f.write(data)
            f.write("\r\n")


def read_region_processed():
    global processed_region
    with codecs.open(processed_region_log, "r", "utf-8") as f:
        for line in f:
            processed_region.append(line)


if __name__ == '__main__':
    # ftp = ftp_connect()
    print "Start to upload"
    result = upload_file(root)
    print "upload done"
    # ftp.quit()
