# -*- coding: utf-8 -*-

# @File:     desc_struc.py
# @Project:  ERP_SYNC
# @Date:     2018/10/23 10:52
# @Author:   ZhangChuan
# @License:  ©2018 mabotech Co.,Ltd. All rights reserved.

import os


class DescStruc:

    @staticmethod
    def read_content(file_path):
        """
        读取文件内容
        :param file_path:       str         文件路径
        :return:                list        文件内容
        """

        with open(file_path, encoding='utf8') as f:
            return f.readlines()

    @staticmethod
    def get_paths(dir_path, depth=None):
        """
        生成器。
        遍历指定目录下的所有非目录文件, 不会列出目录路径。
        注意：这里的路径使用'/'。
        :param dir_path: str/要遍历的目录路径
        :param depth: int/扫描的深度 0:当前目录，1：当前目录的下一级目录
        :return: str/文件路径， 若当前深度下为发现文件，则不返回。
        """
        depth_count = 0

        depth = int(depth) if depth else 0
        dir_path = dir_path if dir_path.endswith('/') else dir_path + '/'

        for path in os.listdir(dir_path):
            tmp_path = dir_path + path

            if os.path.isdir(tmp_path):
                if depth_count < depth:
                    depth_count += 1
                    yield from DescStruc.get_paths(tmp_path + '/', depth - 1)

            else:
                yield tmp_path

    @staticmethod
    def process_content(content):
        """
        处理文本内容为标准格式
        :param content:         list        包含所有字段描述的表结构，每个元素是一行
        :return:                list        标准化的字段描述
        """
        res = []

        for i in content:
            tmp = i.replace('\n', '').split()
            if len(tmp) > 2:
                tmp = [tmp[0], tmp[-1], '{} {}'.format(tmp[1], tmp[2])]

            res.append(tmp)
        return res

    @staticmethod
    def make_sql(tbl_name, frmt_content):
        """
        生成建表语句
        :param tbl_name:            str         表名称
        :param frmt_content:        list        格式化好的字段描述
        :return:                    str         建表语句
        """

        frmt_sql = "CREATE TABLE {}(\n{})"
        fill_str = ''

        for i in frmt_content:
            fill_str += (' '.join(i) + ',\n')
        return frmt_sql.format(tbl_name, fill_str[:-2])

    @staticmethod
    def save_content(content, save_path=None):

        save_path = save_path if save_path else './CREATE_TABLE_SQL.sql'
        """
        保存内容到文件
        :param content:         str          要保存的文件
        :param save_path:       str         保存文件路径
        :return:
        """
        content += '\n\n'
        with open(save_path, 'a', encoding='utf8') as f:
            f.write(content)


def main():
    count = 1
    for i in DescStruc.get_paths('./', 0):
        tbl_name = i.split('/')[-1].split('.')[0].upper()
        if i.split('.')[-1].upper() == 'STRUC':
            res = DescStruc.read_content(i)
            frmt_content = DescStruc.process_content(res)
            sql = DescStruc.make_sql(tbl_name, frmt_content)
            DescStruc.save_content(sql)
            print('[ NO:{} | {} | done.]'.format(count, tbl_name))
            count += 1

    print('[ Total: {} | All work done. ]'.format(count - 1))


if __name__ == "__main__":
    main()
