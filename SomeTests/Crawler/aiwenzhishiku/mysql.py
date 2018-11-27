import MySQLdb
import time

class Mysql:

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def __init__(self):
        try:
            self.db = MySQLdb.connect('localhost','root','123456','test')
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            print self.getCurrentTime(),"Connect to db error, reason: %s" % (e.args[0], e.args[1])

    def insertData(self, table, my_dict):
        try:
            self.db.set_character_set('utf-8')
            cols = ', '.join(my_dict.keys())
            values = '"," '.join(my_dict.values())
            sql = "Insert Into %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()

                if result:
                    return insert_id
                else:
                    return 0
            except MySQLdb.Error, e:
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print self.getCurrentTime(), "Data is exists already and don't insert into DB"
                else:
                    print self.getCurrentTime(),"Insert Data errorm, reason %d: %s" % (e.args[0], e.args[1])
        except MySQLdb.Error, e:
            print self.getCurrentTime(),"DB error, reason %d: %s" % (e.args[0], e.args[1])