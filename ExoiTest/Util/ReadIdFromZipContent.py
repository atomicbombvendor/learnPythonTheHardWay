import re
import zipfile


def read_id_from_zip(file):
    zfile = zipfile.ZipFile(file, 'r')
    pattern = r"(0P[0-9A-Za-z]{8}|0C[0-9A-Za-z]{8})"
    data = set()
    for filename in zfile.namelist():
        content = zfile.read(filename).split("\n")
        for line in content:
            match = re.search(pattern, line)
            if match:
                data.add(match.group())
    return data


if __name__ == "__main__":
    file = "D:\QA\GEDF\R20180809_5728\GEDF\Outputs\Deadwood\NRA\ReferenceNYS\SecurityReference\Monthly\Monthly_SecurityReference_2018-7.zip"
    result = read_id_from_zip(file)
    print ",".join(result)