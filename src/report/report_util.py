# -*- coding: utf-8 -*-

# @File:     report_util.py
# @Project:  Tools
# @Date:     2019/9/10
# @Author:   MaiXiaochai


class ReportUtil:
    def __init__(self, header, data_rows, has_no=True):
        """
        暂时只支持英文标题，中文标题容易错位
        :param header:          list            标题行，不要给出序号列的名称，程序提供
        :param data_rows:       list/tuple      数据，每一个元素是一个数据行
        :param has_no:          Boolean         是否有序号列，默认True，有
        """
        # ==========================================[ Config ]===========================================
        self.NO_NAME = 'NO'                     # 如果有序号列，设置序号列的名称
        self.TITLE_LINE_CHAR = '-'              # 标题行与数据行的分隔线样式
        self.TABLE_LEFT_FILL = ' ' * 3          # 整个表格的左侧填充，没填充则挨着左边缘，很丑
        self.WIDTH_BETWEEN_COLS = 1             # 列间间距(单位，self.BETWEEN_COLS_UNIT)
        self.BETWEEN_COLS_UNIT = ' ' * 4        # 列间填充的基本字符
        self.CELL_FILL_CHAR = ' '               # 单元格填充字符
        # =========================================[ Config end ]========================================

        self.no = has_no
        self.header = ([self.NO_NAME] + header) if self.no else header              # 判断过序号列后的header
        self.rows = data_rows                                                       # 所有数据行组成的列表

        self.header_nbr = len(self.header)                                          # 字段总个数 <= self.cols_nbr
        self.rows_nbr = len(self.rows)                                              # 数据总行数
        self.cols_nbr = max([len(x) for x in self.rows])                            # 数据总列数
        self.between_cols_char = self.BETWEEN_COLS_UNIT * self.WIDTH_BETWEEN_COLS   # 列间填充

    @property
    def __cells_width(self):
        """
        每列的宽度，判断过序号列。
        找出每列的字符的最大宽度作为这列的宽度。
        :return:            list        对应列的宽度,[int, int, ..., int]
        """
        # 首先，比较数据列的宽度
        res = [0] * self.cols_nbr

        calc_list = [self.header[1:] if self.no else self.header] + self.rows

        for i in calc_list:
            for j in range(self.cols_nbr):
                this_width = len(str(i[j]))
                if res[j] < this_width:
                    res[j] = this_width

        # 然后，比较序号列的宽度
        if self.no:
            no_cols_width = max([len(self.NO_NAME), len(str(self.rows_nbr))])
            res = [no_cols_width] + res

        return res

    @property
    def __data_content(self):
        """
        数据行格式化好的内容，先处理基础元素，尽量不改变元素值,但可以改变元素数量
        :return:                    str         格式化好的数据内容
        """

        res = ''
        tmp_list = self.rows

        # 如果有序号列，则给数据行左边加上一个序号
        if self.no:
            tmp_list = [[str(_nbr)] + list(x) for _nbr, x in enumerate(self.rows, 1)]

        for i in tmp_list:
            # 左边填充加到左边
            tmp_row_str = (self.TABLE_LEFT_FILL + self.between_cols_char.join(map(lambda x, y: str(x).ljust(y, self.CELL_FILL_CHAR), i, self.__cells_width)) + '\n')
            res += tmp_row_str

        return res

    @property
    def __title(self):
        """
        表头标题
        :return:                str         表头标题
        """
        title_list = self.header
        res = self.TABLE_LEFT_FILL + self.between_cols_char.join(map(lambda x, y: str(x).ljust(y, self.CELL_FILL_CHAR), title_list, self.__cells_width)) + '\n'
        return res

    @property
    def __title_line(self):
        """
        标题和数据内容间分隔线
        :return:                str           表头和数据内容间分隔线
        """
        _line = self.TITLE_LINE_CHAR * len(self.__title) + '\n'
        return _line

    @property
    def report(self):
        res = '{0}{1}{2}{3}{2}'.format('\n' * 2,
                                       self.__title,
                                       self.__title_line,
                                       self.__data_content)
        return res


def demo():
    headers = ['Order', 'Level', 'start_date']
    data = [
        (1, 2, '2019-9-10 20:00:00'),
        (4, 5, '2019-9-10 20:00:01'),
        (7, 8, '2019-9-10 20:00:02')
    ]
    ru = ReportUtil(headers, data)
    table = ru.report
    print(table)


if __name__ == '__main__':
    demo()
