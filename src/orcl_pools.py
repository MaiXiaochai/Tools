# -*- coding: utf-8 -*-

# @File:     orcl_pools.py
# @Project:  Tools
# @Date:     2018/9/28 10:27
# @Author:   MaiXiaochai

import cx_Oracle as Oracle
from DBUtils.PooledDB import PooledDB


class OrclPool(object):
    """
    这里封装了一些有关oracle连接池的功能

    config样例:
    orcl_cfg = {
    'user': 'user_name',
    'passwd': 'passwd_str',
    'host': 'xxx.xxx.xxx.xxx',
    'port': port_int,
    'sid': 'sid'}
    """

    __pool = None

    def __init__(self, config):
        self.conn = OrclPool.__get_conn(config)
        self.cur = self.conn.cursor()

    @staticmethod
    def __get_conn(conf):
        if OrclPool.__pool is None:

            # mincached：       启动时开启的空连接数量
            # maxcached：       连接池最大可用连接数量
            # maxshared：       连接池最大可共享连接数量
            # maxconnections：  最大允许连接数量
            # blocking：        达到最大数量时是否阻塞
            # maxusage：        单个连接最大复用次数

            dsn = Oracle.makedsn(conf.get('host'), conf.get('port'), conf.get('sid'))
            OrclPool.__pool = PooledDB(Oracle, user=conf['user'], password=conf['passwd'], dsn=dsn,
                                       mincached=5, maxcached=30)

            return OrclPool.__pool.connection()

    def execute_sql(self, sql, args=None):
        """
        执行sql语句
        :param sql:     str     sql语句
        :param args:    list    sql语句参数列表
        :return:
        """

        if args:
            self.cur.execute(sql, args)

        else:
            self.cur.execute(sql)

    def fetch_all(self, sql, args=None):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """

        self.execute_sql(sql, args)
        return self.cur.fetchall()
