# -*- coding: utf-8 -*-

import os


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
                yield from get_paths(tmp_path + '/', depth - 1)

        else:
            yield tmp_path


if __name__ == "__main__":
    the_path = './'
    for i in get_paths(the_path, 2):
        print(i)
