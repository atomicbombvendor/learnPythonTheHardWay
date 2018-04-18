import datetime

import os
import MySQLdb
import sys


def query_data(shareClassId):
    connect = MySQLdb.connect(host="geapidbdev81",
                         port=3306,
                         user="GeDataAgent",
                         passwd="1234567#",
                         db="GEAPI")
    cursor = connect.cursor()
    (operationid, datacategoryid, idtype, productionFrom, status, MiscNotes, Notes, UpdateTime, CreateTime)\
        = (None, None, None, None, None, None, None, None, None)

    sql = "select * from GEAPI.MSSDumpMangement where OperationId='@shareId' and DataCategoryId=105031"
    cursor.execute(sql.replace("@shareId", shareClassId))

    for row in cursor.fetchall():
        operationid = row[0]
        datacategoryid = row[1]
        idtype = row[2]
        productionFrom = row[3].strftime('%Y%m%d')
        status = row[4]
        MiscNotes = row[5]
        Notes = row[6]
        UpdateTime = row[7].strftime('%Y%m%d')
        CreateTime = row[8].strftime('%Y%m%d')
    print('all ', cursor.rowcount, ' records')

    file = "data/test/" + operationid + "/" + UpdateTime + ".dat"
    if file:
        data = "%s, %s, %s, %s, %s, %s, %s, %s, %s" \
            % (operationid, datacategoryid, idtype, productionFrom, status, MiscNotes, Notes, UpdateTime, CreateTime)
    else:
        file = datetime.date.today().strftime('%Y%m%d')
        data = "%s have no data in database" % shareClassId

    write_content(file, data)


def write_content(file, content):
    create_folder(file)
    with open(file, "w+") as f:
        f.write(content)
    print("Write content Done. path: " + file)


def create_folder(path):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)


sids = sys.argv[1:]

if len(sids) ==0:
    print("You must input some shareClassId")

for sid in sids:
    query_data(sid)

# query_data("0P00000003")
