# -*-coding: utf-8 -*-


def nbr_clip(start, end, clip_long):
    """
    将数轴按照 clip_long 的长度切分为 n 个段，返回 左闭右开区间[x, y)，
    最后一个片段的右边界为 end + 1。所以，最好当做 左闭右开区间处理使用，[x, y)
    :param start:           int/数轴起点
    :param end:             int/数轴终点
    :param clip_long:       int/切片长度
    :return:                tuple/当前片段的开始、结束位置(start_int, end_start)
    """
    total_long = end - start
    total_clip = total_long // clip_long + 1

    _left = _right = start

    for i in range(total_clip):
        _left, _right = _right, _right + clip_long
        is_end = _right >= end

        if is_end:
            _right = end + 1

        yield _left, _right

        if is_end:
            break


def demo():
    ls = [1, 2, 3, 4, 5]
    split_array = nbr_clip(1, 5, 2)
    for i in split_array:
        print(i)


if __name__ == "__main__":
    demo()
