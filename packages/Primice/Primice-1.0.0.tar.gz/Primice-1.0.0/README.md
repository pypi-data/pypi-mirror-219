# Primice


# v1.0.0
>2023/07/06
这是我个人使用工具包的1.0.0版本，暂时包含了以下内容：
### MongoDB存储模块
```python
from Primice.Mongo.to_Mongodb import MyMongodb

# 初始化
my_mongodb = MyMongodb(db='test', collection='test', cache_size=60)
```
* 该模块基于pymongo封装
* 该模块提供了基本的增删改查功能
  * 增：`insert_one`, `insert_many`
  * 删：`delete_one`, `delete_many`
  * 改：`update_one`, `update_many`
  * 查：`query`
* 添加了缓存的功能，设定缓存数据的条数，并提供了`insert`方法来插入数据，当缓存数据达到设定的条数时，自动将缓存数据插入到数据库中

### MySQL存储模块

#### 初始化数据库连接
```python
from Primice.MySQL.to_MySQL import MysqlSingleConnect

  # MySQL的配置包含
  # host='localhost', 
  # port=3306, 
  # user='root', 
  # password='', 
  # db(必需), 
  # charset='utf8'
db = MysqlSingleConnect(db='test')
```
#### 初始化数据表

```python
from Primice.MySQL.DataTable import DataTable, data_input

tab = DataTable('test',['id','name','age'])
tab.tab_data.append([1,'张三',18])
```
* 需要了解的是，`DataTable`类与`data_input`是需要配合使用的
* `DataTable`类用于初始化数据表和存储表数据，`data_input`用于向数据库插入数据
* 请注意，`DataTable`的第二个参数列表为插入数据的字段名，当我们向示例的`tab_data`添加数据时，需要保证数据的顺序与字段名的顺序一致
* `data_input`方法的参数为`DataTable`类的实例,同时，需要将初始化的数据库连接传入第二个参数`db`
