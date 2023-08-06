import pymongo

"""
Mongodb存储模块

使用方法：
    1. 实例化对象，传入数据库名和集合名，每个实例化对象对应一个集合 collection
    2. 调用方法
        -- insert_one: 存储单条信息
        -- insert_many: 存储多条信息
        -- query: 查询数据
        -- update_one: 更新数据
        -- update_many: 更新多条数据
        -- delete_one: 删除数据
        -- delete_many: 删除多条数据
"""

class MyMongodb:
    def __init__(self,db:str,collection:str,host='localhost',port=27017,cache_size=60) -> None:
        """
        初始化Mongodb
        :param db: 必须，数据库名
        :param collection: 必须，集合名
        :param host: 远程主机地址，默认为localhost
        :param port: 远程主机端口，默认为27017
        :param cache_count: 缓存数量，默认为60
        """
        self.__client = pymongo.MongoClient(host, port)

        self.__db = self.__client[db]
        self.__collection = self.__db[collection]
        self.__cache_size = cache_size
        self.__cache_list = []

    def set_cache_count(self,count:int):
        if count <= 0:
            raise ValueError("count must be greater than 0")
        elif type(int(count)) != int:
            raise TypeError("count must be int")
        else:
            self.__cache_size = int(count)


    # TODO 自适应插入数据
    def insert(self,data:dict):
        """
        自适应插入数据
        :param data: <dict> 数据
        """
        self.__cache_list.append(data)
        if len(self.__cache_list) >= self.__cache_size:
            self.insert_many(self.__cache_list)
            self.__cache_list.clear()

    # TODO 存储单条信息
    def insert_one(self,data:dict):
        """
        存储单条信息
        :param data: <dict> 数据
        """
        self.__collection.insert_one(data)

    # TODO 存储多条信息
    def insert_many(self,data:list):
        """
        存储多条信息
        :param data: <list> 数据
        """
        self.__collection.insert_many(data)
    
    # TODO 查询数据
    def query(self,query:dict=None, projection:dict=None):
        """
        查询数据
        :param query: <dict> 查询条件
        :param projection: <dict> 查询字段
        """
        return self.__collection.find(query, projection)

    # TODO 更新数据
    def update_one(self,query:dict, data:dict):
        """
        更新数据
        :param query: <dict> 查询条件
        :param data: <dict> 更新数据
        """
        self.__collection.update_one(query,data)
    
    # TODO 更新多条数据
    def update_many(self,query:dict, data:dict):
        """
        更新多条数据
        :param query: <dict> 查询条件
        :param data: <dict> 更新数据
        """
        self.__collection.update_many(query,data)
    
    # TODO 删除数据
    def delete_one(self,query:dict):
        """
        删除数据
        :param query: <dict> 查询条件
        """
        self.__collection.delete_one(query)
    
    # TODO 删除多条数据
    def delete_many(self,query:dict):
        """
        删除多条数据
        :param query: <dict> 查询条件
        """
        self.__collection.delete_many(query)

    # TODO 关闭数据库
    def close(self):
        """
        关闭数据库
        """
        if self.__cache_list:
            self.insert_many(self.__cache_list)
            self.__cache_list.clear()
        self.__client.close()
