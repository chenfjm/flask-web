#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from api import SmsPcode

sms_bp = Blueprint('sms', __name__)
api = Api(sms_bp)

api.add_resource(SmsPcode, '/pcode')
