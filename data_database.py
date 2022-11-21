#向数据库中插入数据
import pandas as pd
import pymysql

def mycursor(db_name=None):
    '''连接数据库，创建游标'''
    # ssl = {'ca': '/path/to/ca/cert'}
    config = dict(zip(['host', 'user', 'port', 'password','ssl_disabled'],
                      ['10.151.144.13', 'root', 30306, 'senseBA2019*',True]))
    print(config)
    config.update(database=db_name)
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    return cursor
print(mycursor(db_name="person"))

def use(db_name):
    '''切换数据库，返回游标'''
    return mycursor(db_name)

def insert_many(table, data):
    '''向全部字段插入数据'''
    val = '%s, ' * (len(data[0])-1) + '%s'
    sql = f'insert into {table} values ({val})'
    cursor.executemany(sql, data)
    cursor.connection.commit()