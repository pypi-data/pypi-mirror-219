
class DataTable:
    """
    通用入库结构
    """
    def __init__(self, tab_name, tab_columns, is_record=True):
        self.tab_name = tab_name  # 表名
        self.tab_columns = tab_columns  # 字段列
        self.tab_data = []  # 二维数据集
        self.is_record = is_record  # 是否记录数据

def data_input(tabs,db):
    """
    通用入库方法
    :param tabs: 数据表
    :param db: 数据库连接,db对象
    """
    if not isinstance(tabs, list):
        tabs = [tabs]
    for tab in tabs:

        tab: DataTable = tab
        if len(tab.tab_data) > 0:
            if tab.is_record:
                ins_sql_template = """insert into {}({}) values({});"""
                ins_sql = ins_sql_template.format(tab.tab_name, ','.join(tab.tab_columns),
                                                  ','.join(['%s'] * (len(tab.tab_columns))))
                db.exec_many(ins_sql, tab.tab_data)
            else:
                ins_sql_template = """insert ignore into {}({}) values({});"""
                ins_sql = ins_sql_template.format(tab.tab_name, ','.join(tab.tab_columns),
                                                  ','.join(['%s'] * (len(tab.tab_columns))))
                db.exec_many(ins_sql, tab.tab_data)
    db.close_db()
