# -*- coding: utf-8 -*-

import os


def get_paths(dir_path):
    """
    生成器。
    遍历指定目录下的所有非目录文件。
    :param dir_path: str/要遍历的目录路径
    :return: str/文件路径
    """

    for path in os.listdir(dir_path):
        tmp_path = dir_path + path

        if os.path.isdir(tmp_path):
                yield from get_paths(tmp_path + '/')

        else:
            yield tmp_path


if __name__ == "__main__":
    the_path = './'
    for i in get_paths(the_path):
        print(i)
