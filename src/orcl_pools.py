# -*- coding: utf-8 -*-

# @File:     orcl_pools.py
# @Project:  Tools
# @Author:   MaiXiaochai
# @Date:     2018/9/28 18:35
# @Modify:   2019/3/28 10:27

import cx_Oracle as Oracle
from DBUtils.PooledDB import PooledDB


class OrclPool(object):
    """
    1) 这里封装了一些有关oracle连接池的功能;
    2) sid和service_name，程序会自动判断哪个有值，
        若两个都有值，则默认使用sid；
        若只想用其中一个，则只需要把另一个设置为空即可。如，service_name = ''

    3) 关于config的设置，注意只有 port 的值得类型是 int，以下是config样例:
        orcl_cfg = {
                    'user': 'user_name_str',
                    'passwd': 'passwd_str',
                    'host': 'xxx.xxx.xxx.xxx_str',
                    'port': port_int,
                    'sid': 'sid_str',
                    'service_name': 'service_name_str'}
    """

    def __init__(self, config):
        self.conn = OrclPool.__get_conn(config)
        self.cur = self.conn.cursor()

    @staticmethod
    def __get_conn(conf):
        """
        一些 PoolDB 中可能会用到的参数，根据实际情况自己选择
        mincached：       启动时开启的空连接数量
        maxcached：       连接池最大可用连接数量
        maxshared：       连接池最大可共享连接数量
        maxconnections：  最大允许连接数量
        blocking：        达到最大数量时是否阻塞
        maxusage：        单个连接最大复用次数

        :param conf:        dict    连接Oracle的信息
        """
        host, port, sid, service_name = conf.get('host'), conf.get('port'), conf.get('sid'), conf.get('service_name')
        
        dsn = None
        if sid:
            dsn = Oracle.makedsn(host, port, sid=sid)
        elif service_name:
            dsn = Oracle.makedsn(host, port, service_name=conf.get('service_name'))

        __pool = PooledDB(Oracle, user=conf['user'], password=conf['passwd'], dsn=dsn, mincached=5, maxcached=30)
        return __pool.connection()

    def execute_sql(self, sql, args=None):
        """
        执行sql语句
        :param sql:     str     sql语句
        :param args:    list    sql语句参数列表
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

    def __del__(self):
        """
        在实例资源被回收时，关闭该连接池
        """
        self.cur.close()
        self.conn.close()


def simple_demo():
    orcl_cfg = {
        'user': 'hello',
        'passwd': 'Python',
        'host': '192.168.158.xxx',
        'port': 1521,
        'sid': '',
        'service_name': 'MaiXiaochai'}

    test_sql = "SELECT COUNT(1) FROM TEST_PYTHON"

    orcl = OrclPool(orcl_cfg)
    orcl.execute_sql(test_sql)
    res = orcl.cur.fetchone()
    print(res)


if __name__ == "__main__":
    simple_demo()
