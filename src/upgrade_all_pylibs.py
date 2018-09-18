# -*- coding: utf-8 -*-

from os import popen


class UpdtPyLibs(object):
    """
    升级所有第三方python库到最新版本
    """

    @staticmethod
    def exec_cmd(cmmd):
        """
        执行命令
        :param cmmd: str/命令内容
        :return: tuple/(boolean, result)
        """
        return popen(cmmd).read()

    @staticmethod
    def get_lib_name(libs_str):
        """
        获得需要升级的pylibs名称列表
        :param libs_str: str
        :return: list/[pylib_name1, pylib_name2, ..., pylibn]
        """
        res = []
        lines = libs_str.split('\n')[2:]
        lines = lines if lines[-1] else lines[:-1]

        for line in lines:
            res.append(line.split()[0])
        return res


def main():
    failed = 0
    cmd_ls = 'pip list --outdated'
    cmd_updt = "pip install -U {}"

    print("Searching libs ...")
    libs_str = UpdtPyLibs.exec_cmd(cmd_ls)
    print("Searching done.")

    libs_name = UpdtPyLibs.get_lib_name(libs_str)
    lib_len = len(libs_name)

    for count, lib in enumerate(libs_name, 1):
        res = 'Succeed'
        cmmd = cmd_updt.format(lib)
        try:
            UpdtPyLibs.exec_cmd(cmmd)

        except Exception as e:
            failed += 1
            res = 'Failed'

        finally:
            report = "[ Name: {}\t| res: {}\t| {}/{}\t| {:.2%} ]".format(lib, res, count, lib_len, count / lib_len)
            print(report)

    final_report = "[UPDATED: {} | FAILED: {} ]".format(lib_len - failed, failed)


if __name__ == '__main__':
    main()
