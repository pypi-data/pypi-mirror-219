# coding=utf-8
"""
vissy@zhu
"""

import pymysql


# 数据库连接
def connectdb(hostname, username, psw, port, dbname):
    connect = pymysql.connect(host=hostname, user=username, password=psw, port=int(port), db=dbname)
    c = connect.cursor()
    return connect, c  # 返回游标，执行sql语句，返回连接参数，是为了执行数据的更新sql，比如update和delete。
