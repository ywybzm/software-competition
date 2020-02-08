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
            except pymysql.Error as e:
                print(e)

        if self.cur is None:
            try:
                self.cur = self.con.cursor()
            except pymysql.Error as e:
                print(e)

    def close_connection(self):
        self.cur = None
        try:
            self.con.close()
        except pymysql.Error as e:
            print(e)
        finally:
            self.con = None

    def query(self, sql):
        print("in db_connect's query(self, sql)方法中，sql语句为%s" % sql)
        data = []
        self.open_connection()
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            print('查询成功')
        except pymysql.Error as e:
            print(e)
        finally:
            self.close_connection()

        return data

    def update(self, sql):
        print("in db_connect's update(self, sql)方法中，sql语句为%s" % sql)
        self.open_connection()
        try:
            self.cur.execute(sql)
            self.con.commit()
            print('更新成功')
        except pymysql.Error as e:
            print(e)
        finally:
            self.close_connection()
