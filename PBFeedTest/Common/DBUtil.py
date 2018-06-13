import pymssql


class LogDB:
    def __init__(self):
        self.url = 'GEGTWKDEVDB8004'
        self.pwd = ''
        self.user = ''
        self.db = 'CalcDB'
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = pymssql.connect(host=self.url, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        self.cur = self.conn.cursor()

    def executeQuery(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def execute(self, sql):
        self.cur.execute(sql)

    def commitChange(self):
        try:
            self.conn.commit()
        except Exception as e:
            print("ERROR, Cannot Commit :", e)

    def close(self):
        self.conn.close()

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            pass


if __name__ == '__main__':
    db = LogDB()
    db.connect()
    db.close()
