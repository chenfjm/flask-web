#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from utils.flask import FlaskUtil
from utils.ecode import ECode
from app.ucenter import uc
from login import LoginService
from user import UserService

fu = FlaskUtil()


@uc.route('/login/phone')
def login_phone():
    phone = request.args.get('phone')
    pcode = request.args.get('pcode')
    unionid = int(request.args.get('unionid'))
    name = request.args.get('name')
    avatar = request.args.get('avatar')
    code, user = LoginService().phone_login(phone, pcode)
    if code == ECode.SUCC:
        sid = fu.login(user)
        res = {
            "user": user,
            "sid": sid
        }
        return fu.result_json(res, code, '')
    elif code == ECode.USER_NOT_EXIST:
        user_srv = UserService()
        user = user_srv.get_user_byunionid(unionid)
        if user:
            user_srv.update_user(user["id"], phone=phone, avatar=avatar)
        else:
            user_info = {
                "name": name,
                "phone": phone,
                "unionid": unionid,
                "avatar": avatar,
            }
            user = user_srv.add_user(user_info)
        sid = fu.login(user)
        res = {
            "user": user,
            "sid": sid
        }
        return fu.result_json(user)
    else:
        return fu.result_json(None, code, '')
