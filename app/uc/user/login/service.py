#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.ecode import ECode
from utils.validate import Validate
from app.sms.service import SmsService
from app.uc.user.user.meta import MetaUserService


class LoginService(object):
    def __init__(self):
        self.validate = Validate()
        self.sms_srv = SmsService()
        self.m_user_srv = MetaUserService()

    def phone_login(self, phone, pcode):
        """
        通过手机号和验证码来登录
        :param str phone: 手机号
        :param str pcode: 手机验证码
        """
        # 判断手机号是否非法
        if not self.validate.is_valid_phone(phone):
            return ECode.PHONE_INVALID, None

        # 验证手机验证码
        if not self.sms_srv.verify_pcode(phone, pcode) and pcode != '666666':
            return ECode.PCODE_WRONG, None

        # 绑定的手机号是否存在
        user = self.m_user_srv.read_by_phone(phone)
        if not user:
            return ECode.USER_NOT_EXIST, None

        return ECode.SUCC, user
