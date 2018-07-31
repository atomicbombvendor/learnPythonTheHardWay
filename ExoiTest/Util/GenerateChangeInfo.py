# coding=utf-8
import codecs
import ConfigParser


def writeFile(file_t, data):
    f = codecs.open(file_t, 'a', 'utf-8')  # w会清空原来的内容 a为追加
    f.write(str(data))
    f.write("\r\n")
    f.close()


def readContent(root, file_t):
    with codecs.open(root + file_t, 'r', 'utf-8') as fr:
        content = fr.read()
    return content


def processContent(file_t, content, template):
    final_content = template.replace("@file@", file_t)
    final_content = final_content.replace("@rn@", "\r\n")
    final_content = final_content.replace("@content@", content)
    return final_content


def truncateFile(file_t):
    with codecs.open(file_t, "w", "utf-8") as f:
        f.truncate()


def generateChangeInfo():
    conf = ConfigParser.ConfigParser()
    conf.read('GenerateChangeInfo_cofig.ini')
    root = conf.get("ChangeInfo_Root", "Root")
    files = conf.get("ChangeInfo_Files", "Files").split(",")
    template = conf.get("ChangeInfo_Template", "Template")
    resultFile = conf.get("ChangeInfo_TargetFile", "TargetFile")
    truncateFile(resultFile)

    for file_t in files:
        print("Start>>> Write " + file_t + "'s ChangeInfo")
        content = readContent(root, file_t)
        final_content = processContent(file_t, content, template)
        writeFile(resultFile, final_content)
        print("End>>> Write " + file_t + "'s ChangeInfo")
    print("End Process All.")


generateChangeInfo()