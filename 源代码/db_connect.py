import pymysql


class DbConnect:

    def __init__(self, host, user, passwd, db, port, charset):
        self.con = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset)
        self.cur = self.con.cursor()

    def get_cursor(self):
        return self.cur

    def close_connection(self):
        self.cur = None
        self.con.close()


