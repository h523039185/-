"""
数据处理数据库交互
"""
import pymysql

class Database:
    def __init__(self,host = "127.0.0.1",
                 port = 3306,
                 user="root",
                 passwd="123456",
                 charset='utf8',
                 database=None):
        self.host = host
        self.port = port
        self.user = user
        self.charset = charset
        self.database = database
        # 连接数据库
        self.db = pymysql.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             password=passwd,
                             database=self.database,
                             charset=self.charset)
    # 生成游标
    def cursor(self):
        self.cur = self.db.cursor()

    def close(self):
        # 使用完毕
        self.cur.close()
        self.db.close()

    # dict_server需要这个类做什么就写什么方法与数据库交互
    def register(self,name,passwd):
        # 验证可否注册
        sql = "select name from user where name=%s"
        self.cur.execute(sql,[name])
        r = self.cur.fetchone() # 获取查询结果
        if r:
            # 查询到内容，用户存在
            return False

        # 插入用户信息
        sql = "insert into user (name,passwd) values \
              (%s,%s)"
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        # 验证可否登录
        sql = "select name from user where name=%s and passwd=%s"
        self.cur.execute(sql,[name,passwd])
        r = self.cur.fetchone() # 获取查询结果
        if r:
            # 查询到内容，用户存在
            return True
        else:
            return False

    # 查询单词
    def query(self,word):
        sql = "select mean from words where word=%s"
        self.cur.execute(sql,[word])
        result = self.cur.fetchone() # Y (mean,) None
        if result:
            return result[0] # 返回解释
        else:
            return "Not Found"

    # 插入历史记录
    def insert_hist(self,name,word):
        sql = "select id from user where name=%s"
        self.cur.execute(sql,[name])
        id = self.cur.fetchone()[0]
        # 插入历史记录
        sql = "insert into hist (word,user_id) values (%s,%s)"
        try:
            self.cur.execute(sql,[word,id])
            self.db.commit()
        except:
            self.db.rollback()

    # 查询历史记录
    def history(self,name):
        sql = "select word,time from hist \
              where user_id=(select id from user where name=%s) \
              order by time desc limit 10;"
        self.cur.execute(sql,[name])
        # ((word,time),(),())
        return self.cur.fetchall()











