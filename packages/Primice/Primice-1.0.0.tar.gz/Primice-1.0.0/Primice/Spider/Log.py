# coding=utf-8
from PycharmProjects.temp_demo.PyPi打包.primice.Primice.MySQL.to_requests import *
from PycharmProjects.temp_demo.PyPi打包.primice.Primice.Mongo.to_Mongodb import *

class Log:
    def __init__(self, options):
        self.__options = {
            "log_level": "WARN",  # 日志等级
            "time_step": 300,  # 日志时间间隔(秒)
            "save_log_to": "mongo",  # 日志保存位置 可选mongo,mysql,file
            "mongo":{
                'host': 'localhost',
                'port': 27017,
            }
        }

        self.__options.update(options)

        self.tab = DataTable('',[])

        self.__mongo = MyMongodb(**self.__options["mongo"])
        self.__mysql = db

        # 用来统计从程序开始到现在的数据
        self.__start_time = time.time()  # 开始时间
        self.__count = 0  # 计数器

        # 用来统计从上次记录日志到现在的数据
        self.__temp_time = time.time()  # 临时时间
        self.__temp_count = 0  # 临时计数器

    def save2mogno(self, log: dict) -> bool|Exception:
        """
        保存日志到mongo
        :param log: 日志
        :return: bool
        """
        pass

    def save2mysql(self, log: list) -> bool|Exception:
        """
        保存日志到mysql
        :param log: 日志
        :return: bool
        """
        data_input(self.tab)


    def save2file(self,path:str, log: str) -> bool|Exception:
        """
        保存日志到文件
        :param path: 文件路径
        :param log: 日志
        :return: bool
        """
        try:
            if self.__options["save_log_to"] == "file":
                file = open(path,'a',encoding='utf-8')
                file.write(log)
            return True
        except Exception as e:
            return e


    def logging(self,**kwargs):
        """
        日志装饰器
        这个方法用来装饰需要记录日志的方法，每隔一段时间记录一次日志
        被装饰的方法执行时间越短越好，否则会影响日志记录的时间间隔
        """
        path = kwargs.get('path')
        def outter(func):
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
                if time.time() - self.__temp_time > self.__options["time_step"]:
                    self.tab.tab_data.append([])
                    func(*args, **kwargs)
                    self.__temp_time = time.time()
            return wrapper
        return outter


if __name__ == '__main__':
    log = Log({
        'time_step': 5
    })


    @log.logging()
    def test(a,b,c):
        time.sleep(1)
        print('test',a,b,c)

    while True:
        test(5,2,1)