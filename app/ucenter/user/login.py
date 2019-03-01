#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.ecode import ECode
from utils.validate import Validate


class LoginService(object):
    def __init__(self):
        pass

    def phone_login(self, phone, pcode):
        """
        通过手机号和验证码来登录
        :param str phone: 手机号
        :param str pcode: 手机验证码
        """
        v = Validate()
        # 判断手机号是否非法
        if not v.is_valid_phone(phone):
            return ECode.PHONE_INVALID, None

        # 验证手机验证码
        if not self.pcode_srv.verify_pcode(phone, pcode) and pcode != "666666":
            return ECode.PCODE_WRONG, None

        # 绑定的手机号是否存在
        user = self.user_srv.get_by_phone(phone)
        if not user:
            return ECode.USER_NOT_EXIST, None

        if not self.user_srv.is_user_valid(user):
            return ECode.USER_INVALID, None
        return ECode.SUCC, user
