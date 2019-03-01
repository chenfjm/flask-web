#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Validate(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Validate, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def is_valid_phone(phone):
        """
        是否是有效的手机号
        :param string phone: 手机号
        """
        if phone.isdigit() and len(phone) == 11:
            return True
        return False

    def is_valid_call_number(phone):
        """
        简单是否是有效的手机号或座机号
        """
        p = re.compile(r'^(?:\+86)?(1\d{10})$|^(?:\+86)?(0\d{2,3})(-)?\d{7,8}$')
        phone_match = p.match(phone)
        if phone_match:
            return True
        return False

    def is_valid_email(email):
        """
        是否是有效的邮箱地址
        :param str email: 电子邮箱
        """
        if re.match(r"^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$", email) is not None:
            return True
        else:
            return False

    def is_chinese(uchar):
        """
        判断一个unicode是否是汉字
        """
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False

    def is_number(uchar):
        """
        判断一个unicode是否是数字
        """
        if uchar >= u'\u0030' and uchar <= u'\u0039':
            return True
        else:
            return False

    def is_alphabet(uchar):
        """
        判断一个unicode是否是英文字母
        """
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or \
                (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True
        else:
            return False
