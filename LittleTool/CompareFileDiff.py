# coding=utf-8
import codecs
import os


def read_file(file1):
    result = []
    with codecs.open(file1, "r") as f:
        for line in f.readlines():
            if "" is not line or line.strip() is not None or line is not "\n" \
                    or line is not "\r\n":
                result.append(line)
            else:
                print "find empty"

    return list(set(result))


# 把data放入set中
def get_set(data):
    result = set()
    if not data:
        return result
    # if getattr(data, '__iter__', None):
    lines = data.split('\r\n')
    for line in lines:
        result.add(line)
    return result


# 比较文件不同，返回比较结果
def compareFiles(old, new):
    sd = set(old)
    sl = set(new)
    return sd - sl, sl - sd


def write_diff(file1, name, content):
    diff_file = os.path.join(os.path.split(file1)[0], os.path.split(file1)[1].replace(".txt", ""), name + ".txt")
    if not os.path.exists(os.path.split(diff_file)[0]):
        os.mkdir(os.path.split(diff_file)[0])

    with codecs.open(diff_file, "w") as f:
        for c in content:
            f.write(c + "\n")
    print "Diff have logged in " + diff_file


def write_content(file1, name, content):
    diff_file = os.path.join(os.path.split(file1)[0], os.path.split(file1)[1].replace(".txt", ""), name + ".txt")
    if not os.path.exists(os.path.split(diff_file)[0]):
        os.mkdir(os.path.split(diff_file)[0])

    with codecs.open(diff_file, "w") as f:
        f.write(content + "\n")
        print "Diff have logged in " + diff_file


def compare_file_diff(file1, file2):
    result_file1 = read_file(file1)
    result_file2 = read_file(file2)
    one_c_tow, tow_c_one = compareFiles(result_file1, result_file2)
    if one_c_tow is None and tow_c_one is None:
        print "there is no diff in " + file1 + " and " + file2 + "\r\n"
    else:
        print "there is some diff in " + file1 + " and " + file2
        write_diff(file1.replace("\\old", ""), "old_diff", one_c_tow)
        write_diff(file2.replace("\\new", ""), "new_diff", tow_c_one)
        print "\r\n"
        if len(result_file1) != len(result_file2):
            write_content(file1.replace("\\old", ""), "size_not_match",
                          "old> " + str(len(result_file1)) + "\r\nnew>" + str(len(result_file2)))


if __name__ == "__main__":
    # old = "D:\QA\AutoComplete\\old\\MS-GERM-SYMBOL-AC-LIST.txt"
    # new = "D:\QA\AutoComplete\\new\\MS-GERM-SYMBOL-AC-LIST.txt"
    # compare_file_diff(old, new)
    root = "D:\QA\AutoComplete\\new"
    for root, dirs, files in os.walk(root, topdown=True):  # topdown 为真，则优先遍历top目录，否则优先遍历top的子目录(默认为开启)
        for file_t in files:
            # if "MS-NORDIC-SYMBOL-AC-LIST.txt" not in file_t:
                file_new = os.path.join(root, file_t)
                file_old = os.path.join(root, file_t).replace("\\new", "\\old")
                compare_file_diff(file_old, file_new)
