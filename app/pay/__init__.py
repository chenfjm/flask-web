#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

pay = Blueprint('pay', __name__)

from weixin import views
