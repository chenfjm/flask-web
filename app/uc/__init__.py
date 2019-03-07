#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from .user.login.view import UserPhoneLogin

uc = Blueprint('ucenter', __name__)
api = Api(uc)

api.add_resource(UserPhoneLogin, '/hello')
