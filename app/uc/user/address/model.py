#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy(current_app)


class AddressModel(db.Model):
    '''
    用户地址
    '''
    __bind_key__ = 'ucenter'
    __tablename__ = 't_address'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False, index=True, comment='uid')
    name = db.Column(db.String(32), nullable=False, default='', comment='姓名')
    phone = db.Column(db.String(16), nullable=False, default='', comment='手机号')
    province = db.Column(db.String(32), nullable=False, comment='省份')
    city = db.Column(db.String(32), nullable=False, comment='城市')
    area = db.Column(db.String(32), nullable=False, comment='地区')
    address = db.Column(db.String(32), nullable=False, default='', comment='详细地址')
    lng = db.Column(db.Numeric(10, 6), default=0.0, comment='经度')
    lat = db.Column(db.Numeric(10, 6), default=0.0, comment='纬度')
    is_default = db.Column(db.Integer, nullable=False, default=0, comment='是否默认地址')
    is_delete = db.Column(db.Integer, nullable=False, default=0, comment='是否删除')
    create_time = db.Column(db.DateTime, nullable=False, index=True, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

