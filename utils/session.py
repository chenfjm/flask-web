#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Session实现
"""
import uuid
import time
import hashlib
import logging
import cPickle as pickle
from flask import request


class SessionManager(object):
    """
    会话管理器
    """
    def __init__(self, secret, backend, cookie_name, domain=None):
        """
        初始化会话管理器
        :param secret: 会话Secret
        :param backend: 后端存储
        :return: None
        """
        self.secret = secret
        self.backend = backend
        self.cookie_name = cookie_name
        self.domain = domain

    def save_session(self, session, expires=0):
        """
        保存会话
        :param session: 会话数据
        :param expires: 失效时间
        :return: None
        """
        data = pickle.dumps(dict(session.items()))
        if len(data) >= 16000:
            logging.warning("hi, man, session(%s) data is too big:%d",
                            session.sid, len(data))
        self.backend.set(session.sid, data)
        self.backend.expire(session.sid, expires)

    def clear_session(self, session):
        """
        清除会话
        :param obj session: 会话数据
        :return: None
        """
        self.backend.delete(session.sid)

    def load_session(self):
        # 会话ID为空, 生成新的Session
        session_id = request.cookies.get('sid') or request.values.get('sid')
        if not session_id:
            session_id = self.gen_session_id()
            return Session(session_id, self)

        # 从后端存储读取Session
        try:
            data = self.backend.get(session_id)
            data = pickle.loads(data) if data else {}
            assert isinstance(data, dict)
        except AssertionError as exp:
            logging.error("session data wrong: %s, %s", data,
                          str(exp), exc_info=True)
            data = {}
        return Session(session_id, self, data)

    def gen_session_id(self):
        """
        生成会话ID
        """
        cont = "%s%s%s" % (uuid.uuid4(), time.time(), self.secret)
        return hashlib.sha1(cont).hexdigest()


class Session(dict):
    """
    会话对象
    """
    def __init__(self, session_id, mgr, data=None):
        """
        初始化会话对象
        :param session_id: 会话ID
        :param mgr: 会话管理器
        :param data: 会话数据
        :return: None
        """
        super(Session, self).__init__()
        self.sid = session_id
        self._mgr = mgr
        self.update(data or {})
        self._change = False

    def save(self, expires=0):
        """
        保存会话数据
        :param expires: 失效时间, 单位为秒
        :return: None
        """
        self._mgr.save_session(self, expires)

    def clear(self):
        """
        清除会话
        @session: 会话数据
        return: None
        """
        self._mgr.clear_session(self)

    def __missing__(self, key):
        """
        Key不存在, 忽略...
        :param key: 会话中的键值
        :return: None
        """
        return None

    def __delitem__(self, key):
        """
        删除数据
        :param key: 会话中的键值
        :return: None
        """
        if key in self:
            super(Session, self).__delitem__(key)

    def __setitem__(self, key, value):
        """
        添加数据
        :param key: 会话中的键值
        :param value: 数据
        :return: None
        """
        super(Session, self).__setitem__(key, value)

    def set(self, key, value, expires=0):
        """
        每次添加数据时, 都序列化到后端存储
        :param key: 会话中的键值
        :param value: 数据
        :param expires: 失效时间
        :return: None
        """
        self[key] = value
        self.save(expires)

