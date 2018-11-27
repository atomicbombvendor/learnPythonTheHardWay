from zipfile import ZipFile, ZIP_DEFLATED

path = "D:\data\\atlasfeed6\GEDF2.0\DailyDelta\GRC\Fundamental\\"
source_z = "DailyDelta_FinancialStatementsBestKnown_2018-11-26.zip"
target_z = "DailyDelta_FinancialStatementsBestKnown_2018-11-20.zip"
source = ZipFile(path + source_z, 'r')
target = ZipFile(path + target_z, 'w', ZIP_DEFLATED)
for file in source.filelist:
    if '2018-11-26' not in file.filename and '2018-11-27' not in file.filename:
        target.writestr(file.filename, source.read(file.filename))
    else:
        new_file_name = file.filename.replace('2018-11-26', '2018-11-20').replace('2018-11-27', '2018-11-20')
        target.writestr(new_file_name, source.read(file.filename))
target.close()
source.close()