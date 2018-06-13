# coding=utf-8
# 一个程序，检查CompanyId是不是在Region中存在。
import codecs
import zipfile
import re

import os


class FindTest:

    def __init__(self):
        self.root = "D:\QA\GEDF\TestDeltaFD\PT2.0_GEDF_180315\\"
        self.real_root = "\\morningstar.com\shares\GeDataFeed\GeDataFeed\DEV\PT2.0_GEDF_180315\\"
        self.companyId = [
            "0C0000AOBJ\tIPM"
        ]
        self.CompanyId = [
            "0C000006U9	EUR",
            "0C000006U9	NRA",
            "0C000006U9	UKI",
            "0C000006UB	EUR",
            "0C000006UB	LTA",
            "0C000006UB	NRA",
            "0C000006UP	EUR",
            "0C000006UP	LTA",
            "0C000006UP	NRA",
            "0C000006UP	UKI",
            "0C00000767	EUR",
            "0C00000767	NRA",
            "0C000007BZ	ASP",
            "0C000007BZ	EUR",
            "0C000007BZ	LTA",
            "0C000007BZ	NRA",
            "0C000007D1	EUR",
            "0C000007D1	NRA",
            "0C000008DE	EUR",
            "0C000008DE	LTA",
            "0C000008DE	NRA",
            "0C000008RC	EUR",
            "0C000008RC	NRA",
            "0C000008TY	NRA",
            "0C000008UQ	ASP",
            "0C000008UQ	EUR",
            "0C000008UQ	LTA",
            "0C000008UQ	NRA",
            "0C000008UQ	UKI",
            "0C0000099W	ASP",
            "0C0000099W	EUR",
            "0C0000099W	LTA",
            "0C0000099W	NRA",
            "0C0000099W	UKI",
            "0C00000BR6	NRA",
            "0C00000BV1	EUR",
            "0C00000BV1	NRA",
            "0C00000C5Z	EUR",
            "0C00000C5Z	NRA",
            "0C00000CFR	ASP",
            "0C00000CFR	EUR",
            "0C00000CFR	NRA",
            "0C00000CKJ	EUR",
            "0C00000CKJ	LTA",
            "0C00000CKJ	NRA",
            "0C00000D8B	ASP",
            "0C00000D8B	EUR",
            "0C00000D8B	NRA",
            "0C00000D8B	UKI",
            "0C00000I6L	EUR",
            "0C00000I6L	NRA",
            "0C00000I8X	EUR",
            "0C00000I8X	NRA",
            "0C00000IEW	EUR",
            "0C00000IEW	NRA",
            "0C00000N9C	EUR",
            "0C00000N9C	NRA",
            "0C00000N9C	UKI",
            "0C00000V3K	ASP",
            "0C00000V3K	EUR",
            "0C00000V3K	NRA",
            "0C00000V4I	ASP",
            "0C00000V4I	EUR",
            "0C00000V4I	NRA",
            "0C00000WVL	ASP",
            "0C00000WVL	EUR",
            "0C00000WVL	NRA",
            "0C00000WVL	UKI",
            "0C00000X7E	EUR",
            "0C00000X7E	NRA",
            "0C00000X7E	UKI",
            "0C00000X84	ASP",
            "0C00000X84	EUR",
            "0C00000X84	NRA",
            "0C00000XCT	ASP",
            "0C00000XUV	ASP",
            "0C00000XUV	NRA",
            "0C00000Y0Y	ASP",
            "0C00000Y0Y	EUR",
            "0C00000Y0Y	NRA",
            "0C00000Y0Y	UKI",
            "0C00000Y1U	ASP",
            "0C00000Y1U	EUR",
            "0C00000Y1U	NRA",
            "0C00000Y1U	UKI",
            "0C00000Y5N	ASP",
            "0C00000Y5N	EUR",
            "0C00000Y5N	NRA",
            "0C00000Y60	ASP",
            "0C00000Y60	EUR",
            "0C00000Y60	NRA",
            "0C00000Y7K	ASP",
            "0C00000Y7K	EUR",
            "0C00000Y8P	ASP",
            "0C00000Y8P	EUR",
            "0C00000Y8P	NRA",
            "0C000014EI	UKI",
            "0C000014HI	ASP",
            "0C00001591	ASP",
            "0C00001591	EUR",
            "0C00001591	NRA",
            "0C00001591	UKI",
            "0C000015CJ	ASP",
            "0C000015CJ	EUR",
            "0C000015CJ	UKI",
            "0C000015CP	ASP",
            "0C000015CP	EUR",
            "0C000015CP	LTA",
            "0C000015CP	NRA",
            "0C000015CP	UKI",
            "0C000015FS	ASP",
            "0C000015FS	NRA",
            "0C00001I1Z	NRA",
            "0C00001J35	ASP",
            "0C00001J35	NRA",
            "0C00001V0U	ASP",
            "0C00002BB1	ASP",
            "0C00003BIC	ASP",
            "0C00003BIC	NRA",
            "0C00003BLO	ASP",
            "0C00003BLO	NRA",
            "0C00003BNC	ASP",
            "0C00003BNC	NRA",
            "0C00003BVV	ASP",
            "0C00004HU6	NRA",
            "0C00004I9L	ASP",
            "0C00004I9L	EUR",
            "0C00004I9L	NRA",
            "0C00004I9U	ASP",
            "0C00004I9U	EUR",
            "0C00004I9U	NRA",
            "0C00008EZD	NRA",
            "0C00008F4K	ASP",
            "0C00008F4K	NRA",
            "0C00008UBL	ASP",
            "0C00008UBL	EUR",
            "0C00008UBL	NRA",
            "0C00008UBL	UKI",
            "0C00008W6Z	EUR",
            "0C00008W6Z	NRA",
            "0C000098YC	ASP",
            "0C00009T8Q	ASP",
            "0C00009T8Q	EUR",
            "0C00009T8Q	NRA",
            "0C0000AIZR	UKI",
            "0C0000AL9V	EUR",
            "0C0000AL9V	NRA",
            "0C0000AN5G	NRA",
            "0C0000AWE9	EUR",
            "0C0000AWE9	LTA",
            "0C0000AWE9	NRA",
            "0C0000AXYU	EUR",
            "0C0000AXYU	NRA",
            "0C0000B0RO	EUR",
            "0C0000B0RO	NRA",
            "0C0000B1NS	EUR",
            "0C0000B1NS	NRA",
            "0C0000B4QR	NRA"] # [] ()
        # {Region}\Fundamental\EarningRatios\Delta
        # {Region}\Fundamental\EarningReports\Delta
        # {Region}\Fundamental\FinancialStatements\Delta
        # {Region}\Fundamental\OperationRatios\Delta
        # {Region}\Fundamental\Segmentation\Delta
        self.floders = {
            # AFR
            "AFR\Fundamental\EarningRatios\Delta": set(),
            "AFR\Fundamental\EarningReports\Delta": set(),
            "AFR\Fundamental\FinancialStatements\Delta": set(),
            "AFR\Fundamental\OperationRatios\Delta": set(),
            "AFR\Fundamental\Segmentation\Delta": set(),

            # ANZ
            "ANZ\Fundamental\EarningRatios\Delta": set(),
            "ANZ\Fundamental\EarningReports\Delta": set(),
            "ANZ\Fundamental\FinancialStatements\Delta": set(),
            "ANZ\Fundamental\OperationRatios\Delta": set(),
            "ANZ\Fundamental\Segmentation\Delta": set(),

            # ASP
            "ASP\Fundamental\EarningRatios\Delta": set(),
            "ASP\Fundamental\EarningReports\Delta": set(),
            "ASP\Fundamental\FinancialStatements\Delta": set(),
            "ASP\Fundamental\OperationRatios\Delta": set(),
            "ASP\Fundamental\Segmentation\Delta": set(),

            # EUR
            "EUR\Fundamental\EarningRatios\Delta": set(),
            "EUR\Fundamental\EarningReports\Delta": set(),
            "EUR\Fundamental\FinancialStatements\Delta": set(),
            "EUR\Fundamental\OperationRatios\Delta": set(),
            "EUR\Fundamental\Segmentation\Delta": set(),

            # IPM
            "IPM\Fundamental\EarningRatios\Delta": set(),
            "IPM\Fundamental\EarningReports\Delta": set(),
            "IPM\Fundamental\FinancialStatements\Delta": set(),
            "IPM\Fundamental\OperationRatios\Delta": set(),
            "IPM\Fundamental\Segmentation\Delta": set(),

            # LTA
            "LTA\Fundamental\EarningRatios\Delta": set(),
            "LTA\Fundamental\EarningReports\Delta": set(),
            "LTA\Fundamental\FinancialStatements\Delta": set(),
            "LTA\Fundamental\OperationRatios\Delta": set(),
            "LTA\Fundamental\Segmentation\Delta": set(),

            # NRA
            "NRA\Fundamental\EarningRatios\Delta": set(),
            "NRA\Fundamental\EarningReports\Delta": set(),
            "NRA\Fundamental\FinancialStatements\Delta": set(),
            "NRA\Fundamental\OperationRatios\Delta": set(),
            "NRA\Fundamental\Segmentation\Delta": set(),

            # UKI
            "UKI\Fundamental\EarningRatios\Delta": set(),
            "UKI\Fundamental\EarningReports\Delta": set(),
            "UKI\Fundamental\FinancialStatements\Delta": set(),
            "UKI\Fundamental\OperationRatios\Delta": set(),
            "UKI\Fundamental\Segmentation\Delta": set()
        }

    # 从Zip文件解析出所有的CompanyId
    def read_id_from_zip(self, file):
        zfile = zipfile.ZipFile(file, 'r')
        pattern = r"(0C[0-9A-Za-z]{8}|0P[0-9A-Za-z]{8})"
        data = []
        for filename in zfile.namelist():
            match = re.search(pattern, filename)
            if match:
                data.append(match.group())
        return data

    # 得到目录下的所有文件完整路径
    def get_all_file(self, file_dir):
        all_file = []
        for root, dirs, files in os.walk(file_dir):
            for f in files:
                if '.zip' in os.path.split(f)[1]:
                    all_file.append(os.path.join(root,f))
        return all_file

    # 把路径下的所有Id读取出来
    def start_read_id(self):
        for key in self.floders.keys():
            path = self.root + key  # 文件夹下有很多压缩包
            all_file = self.get_all_file(path) # 得到所有的压缩包完整路径
            companyId_in_zip = []
            for file in all_file:
                companyId_in_zip.append(self.read_id_from_zip(file)) # 得到压缩包下的所有Id

            func = lambda x,y:x if y in x else x + [y]
            self.floders[key] = reduce(func, [[], ] + companyId_in_zip) # 去重

    # 验证CompanyId在Region下吗
    def check_CompanyId_under_region(self):
        result = ""
        for val in self.CompanyId:
            tmp = val.split("\t")
            id = tmp[0]
            region = tmp[1]
            for key in self.floders.keys():
                if region in key and id in self.floders[key][0]:
                    result += "%s>>%s%s\r\n" % (val, self.real_root, key)
        return result

# find = FindTest()
# find.start_read_id()
# result = find.check_CompanyId_under_region()
# print result
# f = codecs.open("result.dat", "w", "utf-8")
# f.write(result)
# f.close()

# 打印出每个Region\FileType\文件中的Id列表
region = {
    # "AFR",
    # "ASP",
    # "ANZ",
    # "EUR",
    # "IPM",
    # "LTA",
    # "NRA",
    # "UKI"

    "NRA",
    "EUR"
}

fileType = {
    "EarningRatios",
    "EarningReports",
    "FinancialStatements",
    "OperationRatios",
    "Segmentation"
}

path = "D:\QA\GEDF\GEDataFeed-master\GEDF\GenerateFile\Delta\@Region@\Fundamental\@fileType@\Delta"
result = ""
ft = FindTest()
for r in region:
    for t in fileType:
        dir = path.replace("@Region@", r).replace("@fileType@", t)

        files = ft.get_all_file(dir)
        for file in files:
            result += "[%s_%s]\r\n" % (r, re.search("_([A-Za-z]+)_", file).group(1))
            data = ft.read_id_from_zip(file)
            result += "Ids=" + ",".join(data) + "\r\ncount=" + str(len(data)) + "\r\n\r\n"
f = codecs.open("Save_ZipFile_Id_Num.ini", "w", "utf-8")
f.write(result)
f.close()