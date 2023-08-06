#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = '2021/01/14 17:45:54'

import os
from pathlib import PurePath
import datetime


def get_module_path(module):
    return os.path.dirname(module.__file__)


def judge_dir(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            return
        else:
            os.remove(path)
            os.mkdir(path)
    else:
        os.mkdir(path)


def get_now_allfiles(path: str, suffix: list=None):

    assert os.path.exists(path)
    final_pt = []
    for subfn in os.listdir(path):
        if PurePath(subfn).suffix.lower() in suffix:
            final_pt.append(os.path.join(path, subfn))
        else:
            pass

    return final_pt


def abs_file(filename):
    return os.path.abspath(os.path.join(os.getcwd(), filename))


def root_file(filename):
    return os.path.join(os.path.expanduser('~'), filename)


def accord_now_time_create_dir(head_dir='.',
                               prefix_str='',
                               suffix_str='',
                               pass_mkdir=False,
                               to_hour=False,
                               to_minute=False,
                               to_day=False):
    """
    根据当前时间创建文件夹
    :param head_dir: 文件夹的父目录
    :param prefix_str: 文件夹名的前缀
    :param suffix_str: 文件夹名的后缀
    :param pass_mkdir: 是否跳过创建文件夹，只返回文件夹名
    :param to_hour: 时间格式到小时
    :param to_minute: 时间格式到分钟
    :param to_day: 时间格式到天
    :return: 创建的文件夹路径
    """
    now = datetime.datetime.now()
    _fmt = "%Y%m%d_%H.%M.%S.%f"
    if to_hour:
        _fmt = "%Y%m%d_%H"
    if to_minute:
        _fmt = "%Y%m%d_%H.%M"
    if to_day:
        _fmt = "%Y%m%d"
    
    formatted_time = now.strftime(_fmt)
    filename = '_'.join([prefix_str, formatted_time, suffix_str])
    filename = filename[1:] if filename.startswith('_') else filename
    filename = filename[:-1] if filename.endswith('_') else filename

    _p = os.path.abspath(os.path.join(head_dir, filename))
    if os.path.exists(_p):
        print("The dir has existed!")
    else:
        print("Create dir: ", _p)
        if not pass_mkdir:
            os.makedirs(_p)
    return _p
