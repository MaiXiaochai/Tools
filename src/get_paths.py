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


def list_paths(dir_path: str, depth: int = 0, suffix=None, key_str: str = None):
    """
    1) Generator。
    2) 遍历 dir_path 目录下的文件的路径。
    3) 注意：这里的路径使用'/'。
    :param dir_path:    str     要遍历的目录路径
    :param depth:       int     扫描的深度 0:当前目录，1：当前目录的下一级目录
    :param suffix:      str     返回的路径中包含特定后缀，如 ".py" 或者 "py"，默认None，没有后缀限制
    :param key_str:     str     返回的路径中包含特定的关键词
    """

    # 设定当前目录的表示值
    current_dir_level = 0

    dir_path = dir_path if dir_path.endswith("/") else dir_path + "/"

    if suffix:
        if not suffix.startswith('.'):
            suffix = '.' + suffix

    for _path in listdir(dir_path):
        tmp_path = dir_path + _path

        if isdir(tmp_path):
            if current_dir_level < depth:
                yield from list_paths(tmp_path, depth - 1, suffix, key_str)

        else:
            found = []
            if suffix:
                if splitext(tmp_path)[-1] == suffix:
                    found.append(True)
                else:
                    found.append(False)

            if key_str:
                if key_str in tmp_path:
                    found.append(True)
                else:
                    found.append(False)

            if all(found):
                yield tmp_path


def demo():
    test_path = './'
    depth = 0  # 当前目录
    suffix = ".py"  # 搜索后缀为".py"的文件
    key_str = '_'   # 并且路径中包含'_'
    res = list_paths(test_path, depth=depth, suffix=suffix, key_str=key_str)
    for i in res:
        print(i)


if __name__ == "__main__":
    demo()
