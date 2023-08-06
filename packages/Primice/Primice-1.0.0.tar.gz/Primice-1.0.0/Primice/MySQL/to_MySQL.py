import time, pymysql, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用安全请求警告

class MysqlSingleConnect:
    """
    没有结束时自动关闭数据库连接功能，使用时请在调用结束后手动关闭连接
    """

    def __init__(self,db, host='localhost', port=3306, user='root', password='',  charset='utf8'):
        self.conn = None
        self.csr = None
        self.host = host
        self.port = port
        self.username = user
        self.password = password
        self.charset = charset
        self.db = db

        # 数据库连接重试
        retry_num = 0
        while self.conn is None and retry_num <= 100:
            try:
                retry_num += 1
                self._get_connect()
            except Exception as e:
                print(e)
                print('connect error retry:', retry_num, 'sleep 30s!')
                time.sleep(5)

    # TODO 连接数据库，获取游标
    def _get_connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.username, password=self.password,
                                    database=self.db, charset=self.charset)
        self.csr = self.conn.cursor()

    # TODO 查询方法
    def query(self, sql):
        """
        查询方法
        :param sql: 查询语句
        :return: 查询结果
        """
        # print(sql[:2000])
        self.csr.execute(sql)
        return self.csr.fetchall()

    # TODO 执行多条sql语句
    def exec_many(self, sql: str, args: list, print_log=False):
        """
        执行多条sql语句
        :param sql: sql语句
        :param args: 参数
        :param print_log: 是否打印日志
        """
        if print_log:
            print(sql, str(args)[:2000])
            # print('已写入数据库')
        self.csr.executemany(sql, args)
        self.conn.commit()

    # TODO 执行单条sql语句
    def execute(self, sql, args=None, print_log=False):
        """
        执行单条sql语句
        :param sql: sql语句
        :param args: 参数
        :param print_log: 是否打印日志
        """
        if print_log:
            print(sql, str(args)[:2000])
        self.csr.execute(sql, args)
        self.conn.commit()

    def insert(self, sql, args=None):
        """
        插入数据
        :param sql: sql语句
        :param args: 参数
        :return: 插入数据的id
        """
        # print(sql, str(args)[:2000])
        self.csr.execute(sql, args)
        result = self.query('select  LAST_INSERT_ID();')
        self.conn.commit()
        return result[0][0]

    def close_db(self):
        """
        关闭数据库连接
        """
        try:
            self.csr.close()
            self.conn.close()
        except Exception as e:
            print('close connection error ,result:{}'.format(e))
