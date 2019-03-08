#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from .user.login.api import UserPhoneLogin
from user.address.api import Address

uc = Blueprint('ucenter', __name__)
api = Api(uc)

api.add_resource(UserPhoneLogin, '/login/phone')
api.add_resource(Address, '/address/<int:id>')
