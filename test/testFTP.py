# coding=utf-8
import ftplib
from ftplib import FTP

ftp_server = 'ftp.morningstar.com'
ftp_user = 'OnDemandMaster'
ftp_password = 'OnDemandMasterNew1234'
ftp_port = 21
ftp_timeout = 60
ftp_path = '/Equity2/Test'

ftp = FTP()
ftp.connect(ftp_server, ftp_port, ftp_timeout)
ftp.login(ftp_user, ftp_password)
print ftp.getwelcome()
ftp.cwd(ftp_path)

#总结：
'''
文件夹不存在会报错，如果直接使用mkd 是建立在主目录下的。
建立多级目录可以一层层的建，由外到内层。
上传文件时，带上ftp的文件路径。
上传的文件会覆盖吧。

'''
# ftp.cwd("/tst2")  # 文件夹不存在会报错 目录都是建立在主目录下的。
# ftp.mkd("/GeDataFeed") # 文件夹重复创建会报错
# ftp.mkd("/tst3/tst4")  # 一次性创建多个文件夹会报错
# try:
#     ftp.mkd("/Equity2/Test/test1")  # if test1 存在会报错.
# except ftplib.error_perm, e:
#     print e
# ftp.cwd("test1")  # 上传文件需要上传完整的路径？
# # 上传文件需要文件的路径和FTP上的文件夹。 cwd相当于linux上的cd好
# ftp.dir()
# file = "D:\\GEDataFeed\\Monthly\\TWN\\FinancialStatements\\Monthly_FinancialStatementsFinalFirstKnown_0C00000BDL_2018-07\\Monthly_FinancialStatementsFinalFirstKnown_0C00000BDL_2018-08-06.ctrl"
# ftp.storbinary('STOR ' + '22.zip', open(file, 'rb'))
# ftp.dir()
# ftp.mkd("\\GDD3\\GDD4") # 这种方式创建抛出错误
# ftp.mkd("/GDD5/GDD6") # 这种方式创建抛出错误
# ftp.mkd("/GG5") # 这种方式创建没有问题

ftp.cwd('/Equity2/Test/test1/ZWE') # 可以回到主目录
ftp.dir()
# ftp.mkd("/GDD6/GDD7") # 这种方式创建抛出错误
ftp.mkd('/Equity2/Test/test1/ZWE')
ftp.mkd('/Equity2/Test/test1/ZWE/Fundamental') # 一次只能创建一个目录, 通过这种层级关系创建
ftp.dir()
ftp.quit()

