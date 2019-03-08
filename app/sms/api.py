#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource
from utils.flasks import BaseApi
from utils.util import del_dict_key
from service import SmsService


class SmsPcode(Resource, BaseApi):
    def get(self):
        """
        查看某个手机号的当前验证码
        """
        phone = self.get_args('phone')

        code, res = SmsService().get_pcode(phone)
        return self.result_json(res, code)

    def post(self):
        '''
        发送验证码
        '''
        phone = self.get_args('phone')

        # 发送手机验证码
        code, res = SmsService().send_pcode(phone)
        del_dict_key(res, ["pcode"])
        return self.result_json(res, code)

