import zipfile


def read_data_id_from_zip(zip_file):
    zfile = zipfile.ZipFile(zip_file, 'r')

    data_id = set()  # set
    for filename in zfile.namelist():
        for line in zfile.read(filename).split("\r\n"):
            if len(line) > 10:
                data_id.add(line.split("|")[1])

    return data_id


path = "D:\QA\GEDF\MOCAL5177_OperationRatio\GEDF\FTSE100\UKI\Fundamental\OperationRatios\Monthly\Monthly_OperationRatiosAOR_2018-5.zip"

result = read_data_id_from_zip(path)
print sorted(result)