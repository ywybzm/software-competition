import pymysql
from DBUtils.PooledDB import PooledDB

'''
    引入了连接池
    连接池对性能的提升表现在：
        在程序创建连接的时候，可以从一个空闲的连接中获取，不需要重新初始化连接，提升获取连接的速度
        关闭连接的时候，把连接放回连接池，而不是真正的关闭，所以可以减少频繁地打开和关闭连接
'''


class DbConnect:

    def __init__(self, host='', user='', passwd='', db='', port=3306, charset="utf8"):
        self.host = host
        self.user = user
        self.port = int(port)
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.con = None
        self.cur = None
        # 5为连接池里的最少连接数, setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
        self.pool = PooledDB(pymysql, 5, host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port, charset=self.charset,
                             setsession=[
                                 'SET AUTOCOMMIT = 1'])

    def open_connection(self):
        if self.con is None:
            try:
                # 以下是加入DBUtils连接池后的写法
                self.con = self.pool.connection()
                # self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd,
                #                            db=self.db, port=self.port, charset=self.charset)
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
            self.con.rollback()
        finally:
            self.close_connection()
