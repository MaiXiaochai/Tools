#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File:    : del_exit.py
# @Date    : 2019-07-16 16:19:38
# @Author  : MaiXiaochai
# Email    : maixiaochai@outlook.com
# GitHub   : https://github.com/MaiXiaochai
# @Link    : https://maixiaochai.github.io

from re import findall, compile, sub
from os import listdir
from os.path import isdir, splitext
from datetime import datetime


class HandleString:
    """
    删除SQL文件中最后的'EXIT;'
    """
    
    @staticmethod
    def read_data(file_path):
        with open(file_path, 'r', encoding='utf8') as f:
            return f.read()

    @staticmethod
    def save_data(file_path, content, level='w'):
        with open(file_path, level.lower(), encoding='utf8') as op:
            op.write(content)

    @staticmethod
    def read_lines(file_path):
        with open(file_path, 'r', encoding='utf8') as f:
            return f.readlines()

    @classmethod
    def list_path(cls, dir_path, suffix, depth=0):
        """
        Generator
        给出 start_path 目录下， 所有后缀为 suffix 的文件的路径
        :param dir_path:      str         要查找的路径
        :param suffix:        str         要查找的文件后缀
        :param depth:         int         要查找的目录的深度，默认为 0，当前目录
        """
        # 设定当前目录的表示值
        current_dir_level = 0

        dir_path = dir_path if dir_path.endswith("/") else dir_path + "/"
        suffix = suffix if suffix.startswith('.') else '.' + suffix

        for _path in listdir(dir_path):
            tmp_path = dir_path + _path

            if isdir(tmp_path):
                if current_dir_level < depth:
                    yield from cls.list_path(tmp_path, suffix, depth - 1)

            elif splitext(tmp_path)[-1] == suffix:
                yield tmp_path

    @staticmethod
    def handle_content(content):
        """
        处理内容
        :param content:         str     要处理的内容
        :return:                tuple   (boolean, handled_content)
        """
        bad_str = "EXIT;"
        content = content.upper()
        key_nbr = content.count(bad_str)
        bool_val, res_data = False, content

        if key_nbr <= 1:
            bool_val = True
            res_data = content.replace(bad_str, '')

        return bool_val, res_data

    @staticmethod
    def get_time():
        res = datetime.now().strftime("%Y-%m-%d %H:%M")
        return res


def del_exit():
    """
    1）删除SQL文件中最后的'EXIT;'
    2）原理：内容全部大写，然后 count(EXIT;)，
        如果 count(EXIT;)结果 <= 1, 则替换"EXIT;"为空,
        否则，记录路径到 undo_file，便于手工处理
    """
    undo_file = "undo.log"
    hs = HandleString()
    file_path = './'
    res = hs.list_path(file_path, '.sql', 2)

    undo_counter = 1
    for _count, _path in enumerate(res, 1):
        data = hs.read_data(_path)
        res_bool, res_data = hs.handle_content(data)

        if res_bool:
                hs.save_data(_path, res_data)
        else:
            res_data = "[No.{}: {}]\n".format(undo_counter, _path)
            hs.save_data(undo_file, res_data, 'a')
            undo_counter += 1

        log = "[{}][Done][No.{}: {}]".format(hs.get_time(), _count, _path)
        print(log)

    print("Done.")


def distinct():
    """去除重复行"""
    path = "provc.txt"
    save_path = "distinct.txt"
    hs = HandleString()
    res = hs.read_lines(path)

    rp = {sub(r"\[.*any: ", "", x) for x in res}
    content = "".join(list(rp))

    hs.save_data(save_path, content, 'w')


if __name__ == "__main__":
    # main()
    distinct()
