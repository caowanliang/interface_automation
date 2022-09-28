#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/7/21 17:05
# @Author: william.cao
# @File  : mysql_connection.py
# !@Desc : 数据库连接池相关


import pymysql
from dbutils.pooled_db import PooledDB
import logging
import configparser

# 读取数据库配置信息

config = configparser.ConfigParser()
config.read('/config/mss_mysql/mss_db.conf', encoding='UTF-8')
sections = config.sections()
# 数据库工厂
dbFactory = {}
for dbName in sections:
    # 读取相关属性
    maxconnections = config.get(dbName, "maxconnections")
    mincached = config.get(dbName, "mincached")
    maxcached = config.get(dbName, "maxcached")
    host = config.get(dbName, "host")
    port = config.get(dbName, "port")
    user = config.get(dbName, "user")
    password = config.get(dbName, "password")
    database = config.get(dbName, "database")
    databasePooled = PooledDB(creator=pymysql,
                              maxconnections=int(maxconnections),
                              mincached=int(mincached),
                              maxcached=int(maxcached),
                              blocking=True,
                              cursorclass=pymysql.cursors.DictCursor,
                              host=host,
                              port=int(port),
                              user=user,
                              password=password,
                              database=database)
    dbFactory[dbName] = databasePooled


class MySQLConnection(object):
    """
    数据库连接池代理对象
    查询参数主要有两种类型
    第一种：传入元祖类型,例如(12,13),这种方式主要是替代SQL语句中的%s展位符号
    第二种: 传入字典类型,例如{"id":13},此时我们的SQL语句需要使用键来代替展位符,例如：%(name)s
    """

    def __init__(self, dbName="master"):
        self.connect = dbFactory[dbName].connection()
        self.cursor = self.connect.cursor()
        logging.debug("获取数据库连接对象成功,连接池对象:{}".format(str(self.connect)))

    def execute(self, sql, param=None):
        """
        基础更新、插入、删除操作
        :param sql:
        :param param:
        :return: 受影响的行数
        """
        ret = None
        try:
            if param == None:
                ret = self.cursor.execute(sql)
            else:
                ret = self.cursor.execute(sql, param)
        except TypeError as te:
            logging.debug("类型错误")
            logging.exception(te)
        return ret

    def query(self, sql, param=None):
        """
        查询数据库
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回集合
        """
        self.cursor.execute(sql, param)
        result = self.cursor.fetchall()
        return result

    def query_one(self, sql, param=None):
        """
        查询数据返回第一条
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回第一条数据的字典
        """
        result = self.query(sql, param)
        if result:
            return result[0]
        else:
            return None

    def list_by_page(self, sql, current_page, page_size, param=None):
        """
        分页查询当前表格数据
        :param sql: 查询SQL语句
        :param current_page: 当前页码
        :param page_size: 页码大小
        :param param:参数
        :return:
        """
        count_sql = "select count(*) ct from (" + sql + ") tmp "
        logging.debug("统计SQL:{}".format(sql))
        count_num = self.count(count_sql, param)
        offset = (current_page - 1) * page_size
        total_page = int(count_num / page_size)
        if count_num % page_size > 0:
            total_page = total_page + 1
        pagination = {"current_page": current_page, "page_size": page_size, "count": count_num, "total_page": total_page}
        query_sql = "select * from (" + sql + ") tmp limit %s,%s"
        logging.debug("查询SQL:{}".format(query_sql))
        # 判断是否有参数
        if param == None:
            # 无参数
            pagination["data"] = self.query(query_sql, (offset, page_size))
        else:
            # 有参数的情况,此时需要判断参数是元祖还是字典
            if isinstance(param, dict):
                # 字典的情况,因此需要添加字典
                query_sql = "select * from (" + sql + ") tmp limit %(tmp_offset)s,%(tmp_pageSize)s"
                param["tmp_offset"] = offset
                param["tmp_pageSize"] = page_size
                pagination["data"] = self.query(query_sql, param)
            elif isinstance(param, tuple):
                # 元祖的方式
                listtp = list(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"] = self.query(query_sql, tuple(listtp))
            else:
                # 基础类型
                listtp = []
                listtp.append(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"] = self.query(query_sql, tuple(listtp))
        return pagination

    def count(self, sql, param=None):
        """
        统计当前表记录行数
        :param sql: 统计SQL语句
        :param param: 参数
        :return: 当前记录行
        """
        ret = self.query_one(sql, param)
        count = None
        if ret:
            for k, v in ret.items():
                count = v
        return count

    def insert(self, sql, param=None):
        """
        数据库插入
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql, param)

    def update(self, sql, param=None):
        """
        更新操作
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql, param)

    def delete(self, sql, param=None):
        """
        删除操作
        :param sql: 删除SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql, param)

    def batch(self, sql, param=None):
        """
        批量插入
        :param sql: 插入SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.cursor.executemany(sql, param)

    def commit(self, param=None):
        """
        提交数据库
        :param param:
        :return:
        """
        if param == None:
            self.connect.commit()
        else:
            self.connect.rollback()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
        logging.debug("释放数据库连接")
        return None


if __name__ == '__main__':
    connect = MySQLConnection()
