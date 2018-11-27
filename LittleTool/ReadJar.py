# encoding=utf-8

import zipfile


def read_jar_file(jar_path):
    rs1 = []
    zipt = zipfile.ZipFile(jar_path, "r")
    for file_name in zipt.namelist():
        if ".class" in file_name:
            rs1.append(file_name)
    return set(rs1)


def compare_diff(set1, set2):
    return [set1 - set2]


if __name__ == "__main__":
    jar_path = "C:\Users\eli9\Desktop\\feeddeltareceiver_tso.jar"
    jar_path2 = "C:\Users\eli9\Desktop\\feeddeltareceiver.jar"

    rs1 = read_jar_file(jar_path)
    rs2 = read_jar_file(jar_path2)

    print("我的多出来的\r\n")
    rr1 = compare_diff(set(rs2), set(rs1))
    for rr in rr1.pop():
        print rr

    # print("Jean多出来的\r\n")
    # rr1 = compare_diff(set(rs1), set(rs2))
    # for rr in rr1.pop():
    #     print rr