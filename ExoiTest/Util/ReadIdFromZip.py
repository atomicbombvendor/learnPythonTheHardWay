import re
import zipfile


def read_id_from_zip(file):
    zfile = zipfile.ZipFile(file, 'r')
    pattern = r"(0P[0-9A-Za-z]{8}|0C[0-9A-Za-z]{8})"
    data = ''
    for filename in zfile.namelist():
        match = re.search(pattern, filename)
        if match:
            data += match.group() + "\r\n"
    return data

if __name__ == "__main__":
    file = "D:\QA\GEDF\MOCAL5717_AdvisorsV2V3\GEDF\UKI\Reference_v3\Advisor\Monthly\Monthly_Advisor_2018-6.zip"
    result = read_id_from_zip(file)
    print result