#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.sms import sms_bp
from flask import request
from utils.flasks import FlaskUtil
from utils.util import del_dict_key
from .sms import SmsService

fu = FlaskUtil()


@sms_bp.route('/pcode/send')
def send_pcode():
    phone = request.args.get('phone')

    # 发送手机验证码
    code, res = SmsService().send_pcode(phone)
    del_dict_key(res, ["pcode"])
    return fu.result_json(res, code)
