#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy(current_app)


class UserModel(db.Model):
    '''
    用户
    '''
    __bind_key__ = 'ucenter'
    __tablename__ = 't_user'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(36), nullable=False, default='', index=True,
                       comment='第三方用户OPENID')
    openid2 = db.Column(db.String(36), nullable=False, default='', index=True,
                        comment='第三方用户WEAPP OPENID')
    unionid = db.Column(db.String(36), nullable=False, default='', index=True,
                        comment='第三方用户UNIONID')
    name = db.Column(db.String(32), nullable=False, default='', index=True, comment='用户名')
    password = db.Column(db.String(64), nullable=False, default='', comment='密码')
    phone = db.Column(db.String(16), nullable=False, default='', index=True, comment='手机号')
    role = db.Column(db.Integer, nullable=False, default=4, comment='角色')
    sex = db.Column(db.Integer, nullable=False, default=0, comment='性别 0:未知 1:男 2:女')
    avatar = db.Column(db.String(255), nullable=False, default='', comment='头像')
    update_user = db.Column(db.Integer, nullable=False, default=0, comment='更新人id')
    create_time = db.Column(db.DateTime, nullable=False, index=True, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    address = db.relationship('AddressModel', backref='user')

