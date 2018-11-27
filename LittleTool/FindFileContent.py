import codecs
import re


def find_file_content(regex, file_path):
    with codecs.open(file_path, "rb") as f:
        for line in f.readlines():
            matches = re.search(regex, line)
            if matches:
                # print("ESGProduct_%s(\"%s\", \"%s\")," % (matches.group("id"), matches.group("id"), matches.group("name").replace("|\r\n", "")))
                print("idMapping.put(\"%s\", \"%s\");" % (matches.group("name").replace("|\r\n", "").upper(), matches.group("id")))

if __name__ == "__main__":
    regex = "\|(?P<id>[0-9]{6})\|(varchar|bit).*?\|(?P<name>[a-zA-Z_]+)\|\r\n"
    regex2 = r"Data point Name"
    file_path = "C:\Users\eli9\Desktop\\1t.txt"
    find_file_content(regex, file_path)
