#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource
from utils.flasks import UserApi
from utils.ecode import ECode
from service import LoginService
from app.uc.user.user.service import UserService


class UserPhoneLogin(Resource, UserApi):
    def post(self):
        phone = self.get_args('phone')
        pcode = self.get_args('pcode')
        unionid = self.get_args('unionid', '')
        name = self.get_args('name', '')
        avatar = self.get_args('avatar', '')
        code, user = LoginService().phone_login(phone, pcode)
        if code == ECode.SUCC:
            sid = self.login(user)
            res = {
                'user': user,
                'sid': sid
            }
            return self.result_json(res, code, '')
        elif code == ECode.USER_NOT_EXIST:
            user_srv = UserService()
            user = user_srv.get_user_byunionid(unionid)
            if user:
                user_srv.update_user(user['id'], phone=phone, avatar=avatar)
            else:
                user_info = {
                    'name': name,
                    'phone': phone,
                    'unionid': unionid,
                    'avatar': avatar,
                }
                user = user_srv.add_user(user_info)
            sid = self.login(user)
            res = {
                'user': user,
                'sid': sid
            }
            return self.result_json(user)
        else:
            return self.result_json(None, code, '')


