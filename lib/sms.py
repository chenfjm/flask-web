#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
发送短信...
"""
import json
import logging

import sys
from lib.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
reload(sys)
sys.setdefaultencoding('utf8')

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


class SMS(object):
    """
    短信操作类
    """
    def __init__(self, a_key_id=None, a_key_secret=None):
        """
        初始化
        :param smtp: SMTP服务器
        :param user: 用户名
        :param pwd: 密码
        :return: None
        """
        self.a_key_id = a_key_id
        self.a_key_secret = a_key_secret

    def send(self, phone_numbers, sign_name, template_code, template_param=None):
        business_id = uuid.uuid1()
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        template_param = json.dumps(template_param)
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        acs_client = AcsClient(self.a_key_id, self.a_key_secret, REGION)

        # 调用短信发送接口，返回json
        smsResponse = acs_client.do_action_with_exception(smsRequest)
        logging.warn("sms send result: %s", smsResponse)

        # TODO 业务处理

        return smsResponse

if __name__ == "__main__":
    params = {"code": "123456"}
    print SMS().send("13900000000", "云通信测试", "SMS_119085546", params)

