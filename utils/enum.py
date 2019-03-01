#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EnumMetaclass(type):
    """
    枚举元类
    """
    def __new__(mcs, name, bases, attr):
        enum_dict = {}
        for i in attr:
            if not isinstance(attr[i], EnumMem):
                continue
            if attr[i].value in enum_dict:
                raise ValueError("enum value can not repeated:%s", attr[i])
            enum_dict[attr[i].value] = attr[i].desc
            attr[i] = attr[i].value
        attr["__enum_dict__"] = enum_dict
        return type.__new__(mcs, name, bases, attr)

    def __setattr__(cls, name, value):
        """
        禁止设置属性
        """
        raise ValueError("cannot set attr on enum class")


class Enum(object):
    """
    枚举类
    """
    __metaclass__ = EnumMetaclass

    @classmethod
    def values(cls):
        """
        所有枚举值
        :return: 所有枚举值
        """
        return getattr(cls, "__enum_dict__").keys()

    @classmethod
    def dict(cls):
        """
        所有枚举值, 以及说明
        :return: 枚举值－说明
        """
        return getattr(cls, "__enum_dict__")

    @classmethod
    def desc(cls, value, default=None):
        """
        获取对某个值的描述
        :param value: 枚举值
        :return: 说明
        """
        enum_dict = cls.dict()
        if default is not None:
            return enum_dict.get(value, default)
        else:
            return enum_dict[value]

    def __setattr__(self, name, value):
        """
        禁止设置属性
        """
        raise ValueError("cannot set attr on enum instance")

    def __new__(cls, **kargs):
        """
        禁止实例化
        """
        raise ValueError("cannot instaniate enum object")


class EnumMem(object):
    """
    枚举成员类
    """
    def __init__(self, value, desc):
        """
        :param value: 枚举值
        :param desc: 枚举值的描述
        """
        self.value = value
        self.desc = desc

    def __str__(self):
        """
        字符串标示
        """
        return "<enum.EnumMem object %s:%s>" % (self.value, self.desc)

    def __repr__(self):
        """
        自身标示
        """
        return "<enum.EnumMem object %s:%s>" % (self.value, self.desc)

    def __eq__(self, other):
        """
        等于
        """
        if isinstance(other, EnumMem):
            return self.value == other.value
        elif isinstance(other, (int, long)):
            return self.value == other
        else:
            raise

    def __ne__(self, other):
        """
        不等于
        """
        if isinstance(other, EnumMem):
            return self.value != other.value
        elif isinstance(other, (int, long)):
            return self.value != other
        else:
            raise

    def __lt__(self, other):
        """
        小于
        """
        if isinstance(other, EnumMem):
            return self.value < other.value
        elif isinstance(other, (int, long)):
            return self.value < other
        else:
            raise

    def __gt__(self, other):
        """
        大于
        """
        if isinstance(other, EnumMem):
            return self.value > other.value
        elif isinstance(other, (int, long)):
            return self.value > other
        else:
            raise

    def __le__(self, other):
        """
        小于、等于
        """
        if isinstance(other, EnumMem):
            return self.value <= other.value
        elif isinstance(other, (int, long)):
            return self.value <= other
        else:
            raise

    def __ge__(self, other):
        """
        大于、等于
        """
        if isinstance(other, EnumMem):
            return self.value >= other.value
        elif isinstance(other, (int, long)):
            return self.value >= other
        else:
            raise


