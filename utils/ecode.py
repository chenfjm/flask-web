#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
错误码
'''
from .enum import Enum, EnumMem


class ECode(Enum):
    '''
    错误码
    '''
    SUCC = EnumMem(0, '成功')
    PARAM = EnumMem(1, '参数错误')
    INTER = EnumMem(2, '内部错误')
    TIMEOUT = EnumMem(3, '外部接口超时')
    EXTERNAL = EnumMem(4, '外部接口错误')
    RESRC = EnumMem(5, '接口不存在')
    AUTH = EnumMem(6, '鉴权失败')
    FORBID = EnumMem(7, '访问禁止')

    # 用户[1000, 2000]

    USER_NOT_EXIST = EnumMem(1001, '用户不存在')
    USER_EXISTED = EnumMem(1002, '用户已存在')
    NAME_INVALID = EnumMem(1003, '用户名无效')
    PHONE_INVALID = EnumMem(1004, '手机号无效')
    PCODE_WRONG = EnumMem(1005, '验证码错误')
    PCODE_RETRY_LATER = EnumMem(1006, '验证码太频繁')
    NOT_LOGINED = EnumMem(1007, '用户未登录')
    USER_OTHER_LOGIN = EnumMem(1008, '登录被踢出')

    # 账户[2000, 3000]

    ACC_NOT_EXIST = EnumMem(2001, '账户不存在')
    ACC_LOCKED = EnumMem(2002, '账户被锁定')
    ACC_INSUFFICIENT = EnumMem(2003, '账户余额不足')

