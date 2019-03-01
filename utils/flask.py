#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify


class FlaskUtil(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FlaskUtil, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def result_json(data, code=0, msg=''):
        res = {
            'code': code,
            'msg': msg,
            'body': data
        }
        return jsonify(res)
