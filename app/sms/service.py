#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
发送验证码
'''
import time
from flask import current_app
from lib.sms import SMS
from utils.validate import Validate
from utils.context import Context
from utils.ecode import ECode


class SmsService(object):
    '''
    发送验证码逻辑
    '''
    K_PCODE = 'pcode_%s'
    K_PCODE_FAIL = 'pcode_fail_%s'
    K_PCODE_MUTEX = 'pcode_mutex_%s'

    def __init__(self):
        '''
        初始化
        '''
        self.ctx = Context.inst()
        self.cache = self.ctx.cache
        self.valid_srv = Validate()
        SMS_CNF = current_app.config.get('SMS_CNF')
        self.sms_srv = SMS(a_key_id=SMS_CNF['KEY_ID'], a_key_secret=SMS_CNF['KEY_SECRET'])

    def check_frequency_restrict(self, phone):
        '''
        检查发送频度限制
        :param str phone: 手机号
        :return: 业务码, 剩余秒数
        '''
        code = ECode.SUCC

        # 指定的时间之内只能发送一次
        now, remains = int(time.time()), 60 
        pcode_mutex_key = self.K_PCODE_MUTEX % phone
        if not self.cache.set(pcode_mutex_key, now, 60, nx=True):
            last_time = self.cache.get(pcode_mutex_key)
            remains = int(last_time) + 60 - now
            code = ECode.PCODE_RETRY_LATER
        return code, remains

    def fake_send_pcode(self, phone):
        '''
        仅生成验证码, 并不做真实的发送
        :param str phone: 手机号
        :return: pcode
        '''
        return self._gen_pcode(phone)

    def send_pcode(self, phone):
        '''
        发送验证码
        :param str phone: 手机号
        :return: 业务码, {
            'remains': 还剩余多少秒才能继续发送
        }
        '''
        # 判断手机号是否有效
        if not self.valid_srv.is_valid_phone(phone):
            return ECode.PHONE_INVALID, {
                'remains': 0,
            }

        # 频率限制
        code, remains = self.check_frequency_restrict(phone)
        if code != ECode.SUCC:
            return code, {
                'remains': remains,
            }

        # 生成验证码
        pcode = self._gen_pcode(phone)

        # 发送验证码, 记录pcode
        self._send_pcode(phone, pcode)

        return code, {
            'remains': remains,
            'pcode': pcode,
        }

    def _gen_pcode(self, phone):
        '''
        生成验证码, 如果已经存在pcode(2分钟内), 则沿用!
        :param str phone: 手机号
        :return: 验证码
        '''
        pcode = self.cache.get(self.K_PCODE % phone)
        if not pcode:
            pcode = self.ctx.gen_random_code(6)
        self.cache.set(self.K_PCODE % phone, pcode, 120)
        return pcode

    def _send_pcode(self, phone, pcode):
        '''
        发送验证码
        '''
        SMS_CNF = current_app.config.get('SMS_CNF')
        self.sms_srv.send_sms(phone, '真品源', SMS_CNF['TEMPLATE'], {'code': pcode})

    def get_pcode(self, phone):
        '''
        验证手机验证码
        :param str phone: 手机号
        :return: 该手机号当前有效的验证码
        '''
        return self.cache.get(self.K_PCODE % phone)

    def verify_pcode(self, phone, pcode):
        '''
        验证手机验证码
        :param str phone: 手机号
        :param str pcode: 验证码
        :return: True or False
        '''
        # 验证失败次数一小时内, 超过10次, 将被锁定
        fail_key = self.K_PCODE_FAIL % phone
        fail_count = self.cache.get(fail_key) or 0
        if int(fail_count) >= 10:
            return False

        # 校验
        if self.cache.get(self.K_PCODE % phone) == pcode:
            return True

        # TODO: 这里不是原子操作
        if fail_count > 0:
            self.cache.incr(fail_key)
        else:
            self.cache.set(fail_key, 1, 3600)
        return False

