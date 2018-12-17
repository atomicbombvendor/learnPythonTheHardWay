import zipfile


def find_content_from_zip(content, zip_list):
    for z in zip_list:
        zip_t = zipfile.ZipFile(z, 'r', 8)
        file_list = zip_t.namelist()
        for file_t in file_list:
            file_content = zip_t.read(file_t)
            if content in file_content:
                print "find in %s>>%s" % (z, file_t)


if __name__ == '__main__':
    zip_list = [
    ]

    find_content_from_zip("", zip_list)