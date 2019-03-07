#!/usr/bin/env python
# -*- coding: utf-8 -*-


def del_dict_key(dict_data, key_list):
    """
    清空指定键值
    :param obj: 清空的字典
    :param key_list: 要删除的key列表
    :param :return: 清理后的dict
    """
    for key in key_list:
        if key in dict_data:
            del dict_data[key]
    return dict_data


def force_utf8(data):
    """
    数据转换为utf8
    :param data: 待转换的数据
    :param :return: utf8编码
    """
    if isinstance(data, unicode):
        return data.encode("utf-8")
    elif isinstance(data, list):
        return [force_utf8(i) for i in data]
    elif isinstance(data, dict):
        return {force_utf8(i): force_utf8(data[i]) for i in data}
    return data
