#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import datetime
import functools
from flask import request, jsonify, current_app
from utils.session import SessionManager
from utils.ecode import ECode


LOGIN_TYPE_USER = 1
LOGIN_TYPE_ADMIN = 2
AUTH_CNF = current_app.config.get('AUTH_CNF')


class ArgsException(Exception):
    """
    参数异常
    """
    def __init__(self, msg, *args, **kwargs):
        """
        初始化
        """
        super(ArgsException, self).__init__(*args, **kwargs)
        self.msg = msg


class BaseApi(object):
    default_args = object()

    def __init__(self):
        self.current_user = None

    def get_args(self, name, default=default_args):
        value = request.values.get(name)
        if value is None and default == self.default_args:
            raise ArgsException("参数: %s 不能为空" % name)
        if isinstance(value, unicode):
            value = value.encode("utf-8")
        return value

    def get_args_int(self, name, default=default_args):
        """
        获取整型参数
        :param string name: 参数名
        :param list default: 如果未传此参数时得到的默认值
        :return: 返回得到的整型值
        """
        value = self.get_argument(name, default)
        if value == default:
            return value
        try:
            value = int(value)
        except:
            raise ArgsException("参数: %s 格式不正确" % name)
        return value

    def get_args_float(self, name, default=default_args):
        """
        获取浮点型
        :param string name: 名字
        :param list default:
        :return:
        """
        value = self.get_argument(name, default)
        if value == default:
            return value
        try:
            value = float(value)
        except ValueError:
            raise ArgsException("参数: %s 格式不正确" % name)
        return value

    def get_args_datetime(self, name, default=default_args):
        """
        获取时间
        :param name:
        :param default:
        :return:
        """
        value = self.get_argument(name, default)
        if value == default:
            return value
        try:
            value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ArgsException("参数: %s 格式不正确" % name)
        return value

    def get_args_date(self, name, default=default_args):
        value = self.get_argument(name, default)
        if value == default:
            return value
        try:
            value = datetime.datetime.strptime(value, "%Y-%m-%d")
            value = value.date()
        except ValueError:
            raise ArgsException("参数: %s 格式不正确" % name)
        return value

    def get_args_json(self):
        return request.json 

    def result_json(data, code=0, msg=''):
        res = {
            'code': code,
            'msg': msg,
            'body': data
        }
        return jsonify(res)

    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = self.get_current_user()
        return self._current_user

    @property
    def session(self):
        if not hasattr(self, "_session"):
            REDIS_CNF = current_app.config.get('REDIS_CNF')
            session_mgr = SessionManager(AUTH_CNF["cookie_secret"],
                                         redis.Redis(host=REDIS_CNF["session"]["host"],
                                                     port=REDIS_CNF["session"]["port"]),
                                         AUTH_CNF["cookie_name"],
                                         AUTH_CNF["domain"])
            setattr(self, "_session", session_mgr.load_session())
        return getattr(self, "_session")


def login_required(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.send_json(None, ECode.NOT_LOGINED)
        else:
            func(self, *args, **kwargs)
    return wrapper


class UserApi(BaseApi):
    decorators = [login_required]

    def get_current_user(self):
        return self.session.get(AUTH_CNF["user"])

    def login(self, user):
        """
        登录, 记录到SESSION
        """
        self.session[AUTH_CNF["user"]] = {
            "uid": user["id"],
            "openid": user.get("openid", ""),
            "openid2": user.get("openid2", ""),
            "unionid": user.get("unionid", ""),
            "session_key": user.get("session_key", ""),
        }
        self.session.save(2500000)
        return self.session.sid

    def _logout(self, sid=None):
        """
        登出, 清空SESSION
        """
        self.session[AUTH_CNF["user"]] = None
        self.session.save()


class AuthApi(BaseApi):
    decorators = [login_required]

    def login(self, user):
        """
        登录, 记录到SESSION
        """
        self.session[AUTH_CNF["auth"]] = {
            "uid": user["id"],
        }
        self.session.save(2500000)
        return self.session.sid

    def _logout(self, sid=None):
        """
        登出, 清空SESSION
        """
        self.session[current_app.config.get('AUTH_CNF')["auth"]] = None
        self.session.save()

