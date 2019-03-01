#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

uc = Blueprint('ucenter', __name__)

from user import views
