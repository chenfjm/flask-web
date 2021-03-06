#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


DEBUG = False
SECRET_KEY = os.urandom(24)

# redis配置
REDIS_CNF = {
    'session': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
    },
    'base': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 1,
    },
}

AUTH_CNF = {
    "cookie_name": "session_id",
    "cookie_secret": "cccaUI5QAGaDdkL5gEmGeJJFuYh7EQnp2Xdwww",
    "domain": "",
    "user": "session_user",
    "auth": "session_auth",
}

SMS_CNF = {
    'KEY_ID': '',
    'KEY_SECRET': '',
    'TEMPLATE': ''
}
