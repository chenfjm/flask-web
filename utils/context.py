#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
全局资源
'''
import redis
from flask import current_app


class Context(object):
    '''
    全局资源
    '''
    def __init__(self):
        '''
        初始化全局变量
        '''
        # session db
        REDIS_CNF = current_app.config.get('REDIS_CNF')
        self.session = redis.Redis(REDIS_CNF['session']['host'],
                                   REDIS_CNF['session']['port'],
                                   REDIS_CNF['session']['db'])

        # 基础db, 存储用户的自增ID等
        self.cache = redis.Redis(REDIS_CNF['base']['host'],
                                 REDIS_CNF['base']['port'],
                                 REDIS_CNF['base']['db'])

    @staticmethod
    def inst():
        '''
        单例
        '''
        name = '_instance'
        if not hasattr(Context, name):
            setattr(Context, name, Context())
        return getattr(Context, name)

