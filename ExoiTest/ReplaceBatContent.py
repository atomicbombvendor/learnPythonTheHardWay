# coding=utf-8
import codecs
import os


# Root:根目录,获取此目录下的所有文件
# str_old: 要替换的字符串
# str_new: 新的字符串
import re


class ReplaceFileContent:

    def __init__(self):
        self.root = "D:\QA\GEDF\MOCAL5267_Fundmental_EarningReport\TestCase"
        self.file_paths = []
        self.str_old = r"\\morningstar.com\shares\GeDataFeed\GeDataFeed\FTSE100"
        self.str_new = r"D:\QA\GEDF\GeDataFeed-MOCAL4937\GEDF\FTSE100"

    def setRoot(self, root):
        self.root = root

    def setStrOld(self, str_old):
        self.str_old = str_old

    def setStrNew(self, str_new):
        self.str_new = str_new

    # os.path.walk得到文件夹上面的所有文件，不包括目录
    def getAllFiles(self):
        os.path.walk(self.root, self.processDirectory, None)

    # getAllFiles的回调函数，用于向file_paths数组赋值
    def processDirectory(self, args, dirname, filenames):
        for filename in filenames:
            filef = os.path.join(dirname, filename)
            if not os.path.isdir(filef):
                self.file_paths.append(filef)

    # os.walk非递归的方式获取所有的文件路径。
    def getAllFiles2(self):
        for root, dirs, files in os.walk(self.root, topdown=False):
            for filef in files:
                self.file_paths.append(os.path.join(root, filef))

    # 替换文件的内容，全局的。
    def replaceContent(self, file):
        file_data = ""
        with codecs.open(file, 'r', 'utf-8') as f:  # w会清空原来的内容 a为追加
            for line in f.readlines():
                file_data += line.replace(self.str_old, self.str_new)
            self.writeFile(file, file_data)

    @staticmethod
    def writeFile(file_t, data):
        f = codecs.open(file_t, 'w', 'utf-8')  # w会清空原来的内容 a为追加
        f.write(str(data))
        f.close()

    # 全局替换文件内容
    def replaceAllFileContent(self):
        self.getAllFiles2()
        for f in self.file_paths:
            self.replaceContent(f)
            print("Replace " + f + " Done")

    def replace_special(self):
        self.getAllFiles2()
        for f in self.file_paths:
            self.replaceContent_special(f)
            print("Replace " + f + " Done")

    def replace_all_file_type(self, file_type):
        self.getAllFiles2()
        for f in self.file_paths:
            if ".bat" in f:
                if "Delta" not in f:
                    self.replace_file_type(f, file_type)
                    print("Replace " + f + " Done")
                else:
                    pass
            else:
                pass

    def replace_file_type(self, file_t, file_type):
        ft = "/FileType=(.+?)/"

        file_data = ""
        with codecs.open(file_t, 'r', 'utf-8') as f:  # w会清空原来的内容 a为追加
            for line in f.readlines():
                s_old = re.search(ft, line, re.S).group(0)
                s_new = ft.replace("(.+?)", file_type + " ")
                file_data += line.replace(s_old, s_new)

        self.writeFile(file_t, file_data)

    # 替换文件的内容，全局的。
    def replaceContent_special(self, file_t):
        print("Start Replace " + file_t)
        # /AppName=GeDataFeed_Delta 替换为 带有region的。
        # /DeliveryRegions=AFR
        deliveryRegion = "/DeliveryRegions=(\w+)"
        appName = "(/AppName=GeDataFeed_Delta_(\w+)|/AppName=GEDataFeed_Delta_(\w+))"

        file_data = ""
        with codecs.open(file_t, 'r', 'utf-8') as f:  # w会清空原来的内容 a为追加
            for line in f.readlines():
                d = re.search(deliveryRegion, line, re.S).group(0).split("=")[1]
                a = re.search(appName, line, re.S).group(0)
                a_s = a.split("_")
                str_new = a_s[0]+"_"+a_s[1]+"_"+d+"_"+a_s[2]
                if d not in a:
                    file_data += line.replace(a, str_new)

            self.writeFile(file_t, file_data)

    def addAllArguments(self, content):
        self.getAllFiles2()
        for f in self.file_paths:
            self.addArgument(f, content)
            print("Replace " + f + " Done")

    # 当ZipFileDir不存在的时候，把ZipFileDir 参数加入Bat中
    def addArgument(self, file_t, content):
        if ".bat" not in file_t:
            return

        zipDir = "/ZipFilesDir="
        outDir = "/OutputDir="
        IdList = "/IDList="
        dir_t = ""  # 要替换的参数头

        if zipDir in content:
            dir_t = zipDir
        elif outDir in content:
            dir_t = outDir
        elif IdList in content:
            dir_t = IdList

        file_data = ""
        with codecs.open(file_t, 'r', 'utf-8') as f:
            for line in f.readlines():
                if dir_t in line:
                    pass
                else:
                    file_data = "%s %s" % (line, content)

        if file_data:
            self.writeFile(file_t, file_data)


R = ReplaceFileContent()
R.setRoot("D:\QA\GEDF\R20180531_5267_5280\TestCase\\5280")

print("\nSet ZipFileDir & OutputDir")
R.addAllArguments(r"/ZipFilesDir=\\morningstar.com\shares\GeDataFeed\GeDataFeed")
R.addAllArguments(r"/OutputDir=D:\GEDataFeed\Outputs")

# exe
print("\nReplace exe path")
R.setStrOld("D:\GEDataFeed\GeDataFeed_Delta\\bin")
R.setStrNew("D:\QA\GEDF\MOCAL5267_Fin_EarReport\GeDataFeed_Delta\\bin")
R.replaceAllFileContent()

R.setStrOld("D:\GEDataFeed\GeDataFeed_Daily\\bin")
R.setStrNew("D:\QA\GEDF\MOCAL5267_Fin_EarReport\GeDataFeed_Daily\\bin")
R.replaceAllFileContent()

R.setStrOld("D:\GEDataFeed\GeDataFeed_Monthly\\bin")
R.setStrNew("D:\QA\GEDF\MOCAL5267_Fin_EarReport\GeDataFeed_Monthly\\bin")
R.replaceAllFileContent()

# zip file path
print("\nReplace ZipFileDir")
R.setStrOld(r"/ZipFilesDir=\\morningstar.com\shares\GeDataFeed\GeDataFeed")
R.setStrNew(r"/ZipFilesDir=D:\QA\GEDF\R20180531_5267_5280\GEDF")
R.replaceAllFileContent()

# Output folder
print("\nReplace OutputDir")
R.setStrOld(r"/OutputDir=D:\GEDataFeed\Outputs")
R.setStrNew(r"/OutputDir=D:\QA\GEDF\R20180531_5267_5280\Outputs")
R.replaceAllFileContent()

# target file date
print("\nReplace TargetFileDate")
R.setStrOld(r"/TargetFileDate=%1")
R.setStrNew(r"/TargetFileDate=2018-05-24")
R.replaceAllFileContent()

# file type
print("\nReplace File Types")
R.replace_all_file_type("OwnershipDetails")

print("\nAdd IdList")
R.addAllArguments(" /IDList=0P00007NYI,0P0000IL11,0P000080E9,0P000094GI,0P00007OST,0P00007OGF,0P00007O0M,0P000090RG,"
                  "0P00007OI2,0P00007NWB,0P00007O1O,0P00007O8L,0P000090MI,0P00007ODZ,0P00007OQH,0P00007O7R,0P0000EWH9,"
                  "0P00007OQH,0P00007OS9,0P00007P05,0P0000053I,"
                  "0P000002X8,0P000002X8,0P0000BC3A,0P0000B0V8,0P0000B620,0P000009YH,0P0000ART3,0P0000031C,0P000003MH,"
                  "0P000002X8,0P0000JVFF,0P000003X1,0P000002H5,0P000004C0,0P0000032S,0P000002X8,0P0000BDBJ,0P0000B0V8,"
                  "0P000003IJ /IDType=2 /CompanyIDList=0C000006U3,0C000006UP,"
                  "0C0000B0J0,0C0000AJJU,0C0000AJ2H,0C00006JXN,0C0000693J,0C000051BO,0C00004IB2,0C00004I9L,0C00004DLV,"
                  "0C00003APD,0C0000A7PW,0C0000A6T2,0C00006JXN,0C00006HXD,0C00006DQ5,0C000051BO,0C00003CVJ,"
                  "0C0000B0J0,0C00008WVR,0C00008OCJ,0C00006JXN,0C00006HXD,0C00006DQ5,0C000051BO,0C00003BJ7,0C00002JWR,"
                  "0C000015CU,0C00002BE2,0C0000158L,0C00000XUF,0C0000A6T2,0C00008I7X,0C00006INA,0C00006HXD,0C00006DQ5,"
                  "0C00004I9L,0C000048K5,0C00003CVJ,0C00003BJ7,0C00003APD,0C000006U3,0C000006UP,0C000006UX,0C000006ZW,"
                  "0C0000070W,0C0000070X,0C0000071S,0C000007BU,0C000007BZ,0C000007W1,0C000006UX,0C000006ZW,0C0000070W,"
                  "0C0000070X,0C0000071S,0C00000768,0C000007BU,0C000007W1,0C0000086M,0C000008EC,0C000006U3,0C000006UP,"
                  "0C000007BU,0C000007BZ,0C0000084T,0C000008EC,0C000008G5,0C000008U7,0C000009DD,0C000009K4,0C00000QR4,"
                  "0C00000PLC,0C00000L54,0C00000I5X,0C00000EY8,0C00000C96,0C00000AWW,0C00000ADA,0C000009SE,0C000009FQ,"
                  "0C000007BU,0C000009SE,0C00000ADA,0C00000AWW,0C000007BU,0C000009SE,0C00000ADA,0C0000BCKX,0C0000BCKF,"
                  "0C0000BC5C,0C0000BBYR,0C0000BBR8,0C0000BAKL,0C0000BAGY,0C0000B9VL,0C0000B9UV,0C0000B9QE,0C0000BCKX,"
                  "0C0000BCKF,0C0000BBYR,0C0000BBR8,0C0000BAKL,0C0000BAGY,0C0000B9VL,0C0000B9QE,0C0000B9LZ,0C0000B9HY,"
                  "0C0000AO6T,0C0000AJJU,0C0000A7PW,0C00008OCJ,0C00008I7X,0C00008HNN,0C00006JXN,0C00006HXD,0C00004IB2,"
                  "0C00004DLV,0C00008Q21,0C00006HXD,0C000038M1,0C000037D8,0C000017FS,0C000015J9,0C000015IA,0C000015BU,"
                  "0C0000158J,0C0000156F,0C0000A6T2,0C000099VF,0C00008Q21,0C00008HNN,0C00006HXD,0C000051BO,0C00003C77,"
                  "0C000038M1,0C000037D8,0C000017FS,0C0000693J,0C00002JWR,0C00002C85,0C000015WV,"
                  "0C000015CW,0C000015CP,0C000015CH,0C0000158L,0C00000ZZU,0C00000X63 ")