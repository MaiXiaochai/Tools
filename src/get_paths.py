#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File:    : get_paths.py
# @Date    : 2019-07-17 16:19:38
# @Author  : MaiXiaochai
# Email    : maixiaochai@outlook.com
# GitHub   : https://github.com/MaiXiaochai
# @GitPage : https://maixiaochai.github.io

from os import listdir
from os.path import isdir, splitext


def list_paths(dir_path, depth=0, suffix=None):
    """
    1) Generator。
    2) 遍历 dir_path 目录下 所有后缀为 suffix 的文件的路径。
    3) 注意：这里的路径使用'/'。
    :param dir_path:    str     要遍历的目录路径
    :param depth:       int     扫描的深度 0:当前目录，1：当前目录的下一级目录
    :param suffix:      str     文件后缀，如 ".py" 或者 "py"
    :return:            str     文件路径
    """

    # 设定当前目录的表示值
    current_dir_level = 0

    dir_path = dir_path if dir_path.endswith("/") else dir_path + "/"
    suffix = suffix if suffix.startswith('.') else '.' + suffix

    for _path in listdir(dir_path):
        tmp_path = dir_path + _path

        if isdir(tmp_path):
            if current_dir_level < depth:
                yield from list_paths(tmp_path, depth - 1, suffix)

        elif splitext(tmp_path)[-1] == suffix:
            yield tmp_path


def demo():
    test_path = './'
    depth = 1       # 当前目录和下一级目录
    suffix = "py"   # 搜索后缀为"py"的文件
    res = list_paths(test_path, depth, suffix)
    for i in res:
        print(i)


if __name__ == "__main__":
    demo()
