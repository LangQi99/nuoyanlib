# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-07-02
#
# ====================================================


from re import match as _match
from .._core._sys import is_client as _is_client


__all__ = [
    "add_condition_to_func",
    "remove_condition_to_func",
    "all_indexes",
    "check_string",
    "check_string2",
    "turn_dict_value_to_tuple",
    "turn_list_to_tuple",
    "is_method_overridden",
    "translate_time",
]


def _get_lib_system():
    if _is_client():
        from .._core._client._lib_client import get_lib_system
    else:
        from .._core._server._lib_server import get_lib_system
    return get_lib_system()


def add_condition_to_func(cond, func, freq=1):
    """
    | 为指定函数添加一个条件，当条件发生变化时，自动执行一次函数。例如，当条件由 ``True`` 变化到 ``False``，或由 ``False`` 变化到 ``True`` 时，都会执行一次指定函数。

    -----

    :param function cond: 条件函数，无参数，需要返回一个bool，当返回的bool（即条件）发生变化时，自动执行一次func
    :param function func: 条件发生变化时执行的函数，该函数需要接受一个类型为bool的参数，即当前的条件状态（cond的返回值）
    :param int freq: 条件判断频率，单位为tick，默认为1，即每1tick判断一次，小于1的值会被视为1

    :return: 返回一个int型ID，后续可用该ID移除添加的条件和函数，添加失败时返回-1
    :rtype: int
    """
    freq = max(1, int(freq))
    lib_sys = _get_lib_system()
    if not lib_sys:
        return -1
    return lib_sys.add_condition_to_func(cond, func, freq)


def remove_condition_to_func(cond_id):
    """
    | 移除由 ``add_condition_to_func`` 添加的条件和函数。

    -----

    :param cond_id: 由add_condition_to_func返回的ID

    :return: 是否成功
    :rtype: bool
    """
    lib_sys = _get_lib_system()
    if not lib_sys:
        return False
    return lib_sys.remove_condition_to_func(cond_id)


def all_indexes(seq, *elements):
    """
    | 获取元素在序列中所有出现位置的下标。
    
    -----

    :param Sequence seq: 任意序列，可以是列表、元组、字符串等
    :param Any elements: 待查找元素

    :return: 元素所有出现位置的下标列表
    :rtype: list[int]
    """
    return [i for i, e in enumerate(seq) if e in elements]


def check_string(string, *check):
    """
    | 检测字符串是否只含有指定字符。
    
    -----

    :param str string: 字符串
    :param str check: 检测元素，可用"0-9"表示所有数字，"a-z"表示所有小写字母，"A-Z"表示所有大写字母

    :return: 只含有指定字符则返回True, 否则返回False
    :rtype: bool
    """
    for i in string:
        if "a-z" in check and _match("[a-z]", i):
            continue
        if "A-Z" in check and _match("[A-Z]", i):
            continue
        if "0-9" in check and _match("[0-9]", i):
            continue
        if i in check:
            continue
        return False
    return True


def check_string2(string, *check):
    """
    | 返回字符串中指定字符之外的字符的列表。
    
    -----

    :param str string: 字符串
    :param str check: 检测元素，可用"0-9"表示所有数字，"a-z"表示所有小写字母，"A-Z"表示所有大写字母

    :return: 指定字符之外的字符的列表
    :rtype: list[str]
    """
    result = []
    for i in string:
        if i in check:
            continue
        if "a-z" in check and _match("[a-z]", i):
            continue
        if "A-Z" in check and _match("[A-Z]", i):
            continue
        if "0-9" in check and _match("[0-9]", i):
            continue
        result.append(i)
    return result


def turn_dict_value_to_tuple(orig_dict):
    """
    | 将字典值中的列表全部转换为元组。（改变原字典）
    
    -----

    :param dict orig_dict: 字典

    :return: 无
    :rtype: None
    """
    for key, value in orig_dict.items():
        if isinstance(value, list):
            orig_dict[key] = turn_list_to_tuple(value)


def turn_list_to_tuple(lst):
    """
    | 将一个列表及其元素中的列表转换成元组。
    
    -----

    :param list lst: 列表

    :return: 转换后的元组
    :rtype: tuple
    """
    new_lst = []
    for i in lst:
        if isinstance(i, list):
            new_lst.append(turn_list_to_tuple(i))
        else:
            new_lst.append(i)
    return tuple(new_lst)


def is_method_overridden(subclass, father, method):
    """
    | 判断子类是否重写了父类的方法。
    
    -----

    :param Any subclass: 子类
    :param Any father: 父类
    :param str method: 方法名

    :return: 方法被重写返回True，否则返回False
    :rtype: bool
    """
    subclass_method = getattr(subclass, method)
    father_method = getattr(father, method)
    return subclass_method != father_method


def translate_time(sec):
    """
    | 将秒数转换成h/m/s的格式。
    
    -----

    :param int sec: 秒数

    :return: h/m/s格式字符串
    :rtype: str
    """
    if sec <= 60:
        return "%ds" % sec
    elif 60 < sec < 3600:
        m = sec // 60
        s = sec - m * 60
        return "%dm%ds" % (m, s)
    else:
        h = sec // 3600
        m = (sec - h * 3600) // 60
        s = sec - h * 3600 - m * 60
        return "%dh%dm%ds" % (h, m, s)


if __name__ == "__main__":
    print all_indexes([1, 1, 4, 5, 1, 4], 1)  # [0, 1, 4]
    print all_indexes([1, 1, 4, 5, 1, 4], 1, 4)  # [0, 1, 2, 4, 5]
    print all_indexes("abcdefg", "c", "g")  # [2, 6]
    print "-" * 50
    print check_string("11112222", "1", "2")  # True
    print check_string("11112222", "1")  # False
    print check_string("1234567890", "0-9")  # True
    print check_string2("abc123", "a", "c", "3")  # ["b", "1", "2"]
    print check_string2("abc123", "a-z")  # ["1", "2", "3"]
    print check_string2("abc123", "0-9")  # ["a", "b", "c"]
    print "-" * 50
    a = {'b': [1, 2, 3], 'c': "hahaha", 'd': [4, 5]}
    turn_dict_value_to_tuple(a)
    print a  # {'b': (1, 2, 3), 'c': "hahaha", 'd': (4, 5)}
    a = [1, [2, 3], "abc"]
    print turn_list_to_tuple(a)  # (1, (2, 3), "abc")
    print "-" * 50
    class A:
        def printIn(self, s):
            print s
    class B(A):
        def printIn(self, s):
            print 1
    class C(A):
        pass
    print is_method_overridden(B, A, "printIn")  # True
    print is_method_overridden(C, A, "printIn")  # False
    print "-" * 50
    print translate_time(4000)  # "1h6m40s"
    print "-" * 50
    print 2 / 3.0


























