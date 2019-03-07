#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = True


SQLALCHEMY_DATABASE_URI = 'mysql://web:web123456@127.0.0.1:3306/smart'
SQLALCHEMY_BINDS = {
    'ucenter': 'mysql://web:web123456@127.0.0.1:3306/ucenter',
    'account': 'mysql://web:web123456@127.0.0.1:3306/account',
    'pay': 'mysql://web:web123456@127.0.0.1:3306/pay',
}
