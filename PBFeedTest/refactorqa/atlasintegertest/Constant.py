import os

rootQAFolder = os.path.join('/', 'QA', 'AtlasIntegerTest')
onEvPackage = os.path.join('/', 'QA', 'AtlasIntegerTest', 'onEnvironment', 'feedbuilder.jar')
offEvPackage = os.path.join('/', 'QA', 'AtlasIntegerTest', 'offEnvironment', 'feedbuilder.jar')

offEvConfigPath = os.path.join('/', 'QA', 'AtlasIntegerTest', 'offEnvironment', 'config/')
onEvConfigPath = os.path.join('/', 'QA', 'AtlasIntegerTest', 'onEnvironment', 'config/')

onEvComparePath = os.path.join('/', 'QAData', 'on', 'data', 'feed', 'file')
offEvComparePath = os.path.join('/', 'QAData', 'off', 'data', 'feed', 'file')

compareResult = os.path.join('/', 'QA', 'AtlasIntegerTest')
onEvResult = os.path.join(compareResult, "onEvResult.txt")
offEvResult = os.path.join(compareResult, "offEvResult.txt")

onEvCompareResult = os.path.join(compareResult, "notInOn.txt")
offEvCompareResult = os.path.join(compareResult, "notInOff.txt")

filters = {os.path.join("QAData", "on"), os.path.join("QAData", "off")}
