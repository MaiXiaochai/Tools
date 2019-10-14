# -*- coding: utf-8 -*-

# @File     : logger.py
# @Project  : downloader_script
# @Software : PyCharm
# @Version  : 1.0
# @Date     : 2018/4/25 13:48
# @Author   : Maixiaochai
# @Email    : maixiaochai@outlook.com

from os import makedirs, path

from logbook.more import ColorizedStderrHandler
from logbook import set_datetime_format, Logger, RotatingFileHandler

from public_funcs import pf


class MyLog:
    """
    把logbook封装了一下，做了一些定制。
    > 日志文件现在用固定的名称；
    > 可以设置单个日志文件大小和总的备份日志数量；
    > 日志在终端显示为定制颜色（我怎么只看到了红色）。
    > 2019-5-14 10:17:38
    """

    def __init__(self, log_folder, log_name=None, max_size=100, backup_count=10):
        """
        log_folder:     日志文件夹
        log_name:       日志文件名称
        max_size:       单个日志文件的大小，单位 MB
        backup_count:   总备份数量，默认为 5
        log_path:       日志文件全路径

        注意：所有 handler 中的 bubble 表示记录是否给下个 handler 用。
        """
        # 设置日志信息时间的格式
        set_datetime_format('local')

        self.log_folder = log_folder
        self.log_name = str(log_name) if log_name else 'pms'
        self.log_path = self.__file_path()

        # 检查存放日志的文件夹是否存在，不存在则创建
        self.__check_path()

        self.log_ = Logger(self.log_name.split('.')[0])
        self.log_.handlers.append(RotatingFileHandler(filename=self.log_path,
                                                      mode='a',
                                                      level='INFO',
                                                      max_size=max_size * 1024 ** 2,
                                                      backup_count=backup_count,
                                                      bubble=True))
        self.log_.handlers.append(ColorizedStderrHandler(bubble=False))

    def __check_path(self):
        """
        这里会自动创建log日志文件夹(如果不存在则创建)，
        日志文件会放到日志文件夹里
        """

        if not path.exists(self.log_folder):
            makedirs(self.log_folder)

    def __file_path(self):
        res = path.join(self.log_folder, self.log_name).replace('\\', '/')
        return res

    def log(self, content):
        """
        定制的log记录、显示功能
        demo: [2017-11-02 10:50:10.468873] INFO: pms_downloader: Hello, python!
        """
        content = "[ {} ]".format(str(content))
        self.log_.info(content)


# ================[ log config ]=====================
# log_folder:     日志文件夹
# log_name:       日志文件名称
# max_size:       单个日志文件的大小，单位 MB
# backup_count:   总备份数量，默认为 5
# ===================================================

log_cfg = {
    'log_folder': '',
    'log_name': 'mes_191010',
    'max_size': 20,
    'backup_count': 5,

}
folder = log_cfg.get('log_folder')
name = log_cfg.get('log_name')
max_size = log_cfg.get('max_size')
backup_count = log_cfg.get('backup_count')

log = MyLog(folder, name, max_size, backup_count).log
