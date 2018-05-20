# coding=utf-8
import codecs
import os


# Root:根目录,获取此目录下的所有文件
# str_old: 要替换的字符串
# str_new: 新的字符串
import re


class ReplaceFileContent:

    def __init__(self):
        self.root = "D:\QA\GEDF\GeDataFeed-MOCAL4169\TestCase"
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
    def writeFile(file, data):
        f = codecs.open(file, 'w', 'utf-8')  # w会清空原来的内容 a为追加
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
            if "Delta" not in f:
                self.replace_file_type(f, file_type)
                print("Replace " + f + " Done")
            else:
                pass

    def replace_file_type(self, file, file_type):
        ft = "/FileType=(.+?)/"

        file_data = ""
        with codecs.open(file, 'r', 'utf-8') as f:  # w会清空原来的内容 a为追加
            for line in f.readlines():
                s_old = re.search(ft, line, re.S).group(0)
                s_new = ft.replace("(.+?)", file_type + " ")
                file_data += line.replace(s_old, s_new)

            self.writeFile(file, file_data)

    # 替换文件的内容，全局的。
    def replaceContent_special(self, file):
        print("Start Replace " + file)
        # /AppName=GeDataFeed_Delta 替换为 带有region的。
        # /DeliveryRegions=AFR
        deliveryRegion = "/DeliveryRegions=(\w+)"
        appName = "(/AppName=GeDataFeed_Delta_(\w+)|/AppName=GEDataFeed_Delta_(\w+))"

        file_data = ""
        with codecs.open(file, 'r', 'utf-8') as f:  # w会清空原来的内容 a为追加
            for line in f.readlines():
                d = re.search(deliveryRegion, line, re.S).group(0).split("=")[1]
                a = re.search(appName, line, re.S).group(0)
                a_s = a.split("_")
                str_new = a_s[0]+"_"+a_s[1]+"_"+d+"_"+a_s[2]
                if d not in a:
                    file_data += line.replace(a, str_new)

            self.writeFile(file, file_data)


R = ReplaceFileContent()
R.setRoot("D:\QA\GEDF\GeDataFeed-MOCAL4724\TestCase\Monthly")

# exe
# R.setStrOld("D:\GEDataFeed\GeDataFeed_Delta\\bin")
# R.setStrNew("D:\QA\GEDF\GeDataFeed-master\GeDataFeed_Delta\\bin")
# R.replaceAllFileContent()

# R.setStrOld("D:\GEDataFeed\GeDataFeed_Daily\\bin")
# R.setStrNew("D:\QA\GEDF\GeDataFeed-MOCAL4724\GeDataFeed_Daily\\bin")
# R.replaceAllFileContent()

R.setStrOld("D:\GEDataFeed\GeDataFeed_Monthly\\bin")
R.setStrNew("D:\QA\GEDF\GeDataFeed-MOCAL4724\GeDataFeed_Monthly\\bin")
R.replaceAllFileContent()

# zip file path
R.setStrOld(r"/ZipFilesDir=\\morningstar.com\shares\GeDataFeed\GeDataFeed")
R.setStrNew(r"/ZipFilesDir=D:\QA\GEDF\GeDataFeed-MOCAL4724\GEDF")
R.replaceAllFileContent()

# Output folder
R.setStrOld(r"/OutputDir=D:\GEDataFeed\Outputs\Deadwood")
R.setStrNew(r"/OutputDir=D:\QA\GEDF\GeDataFeed-MOCAL4724\Outputs\Deadwood")
R.replaceAllFileContent()

# target file date
R.setStrOld(r"/TargetFileDate=%1")
R.setStrNew(r"/TargetFileDate=2018-05-03")
R.replaceAllFileContent()

# file type
R.replace_all_file_type("CompanyReference,SecurityReference,CompanyReference_v2,SecurityReference_v2,CompanyReference_v3,SecurityReference_v3")