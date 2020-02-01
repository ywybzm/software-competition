import pymysql


class DbConnect:

    def __init__(self, host='', user='', passwd='', db='', port='', charset="utf8"):
        self.host = host
        self.user = user
        self.port = int(port)
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.con = None
        self.cur = None

    def open_connection(self):
        if self.con is None:
            try:
                self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd,
                                           db=self.db, port=self.port, charset=self.charset)
            except:
                pass

        if self.cur is None:
            try:
                self.cur = self.con.cursor()
            except:
                pass

    def close_connection(self):
        self.cur = None
        try:
            self.con.close()
        except:
            pass
        finally:
            self.con = None

    def query(self, sql):
        data = []
        self.open_connection()
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
        except:
            pass
        finally:
            self.close_connection()

        return data

    def update(self, sql, data):
        self.open_connection()
        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except:
            pass
        finally:
            self.close_connection()
